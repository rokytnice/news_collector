#!/usr/bin/env python3
"""
Deterministische Werkzeuge fuer die News-Collector-Agenten.

Dieses Modul enthaelt BEWUSST keine LLM-Logik. Relevanzbewertung und Uebersetzung
machen die Claude-Agenten in `.claude/agents/` selbst — hier liegt nur, was
deterministisch ist und in einem Agenten reine Verschwendung waere:
RSS holen, Zeitfenster, Keyword-Vorfilter, Deduplizierung, HTML-Rendering.

Subcommands:
  fetch   RSS-Feeds holen, filtern, deduplizieren -> JSONL mit Kandidaten
  render  finale Artikel (JSONL) -> HTML-Report
"""

import argparse
import html
import importlib
import json
import logging
import re
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import feedparser
import requests

logger = logging.getLogger("feed_tools")

USER_AGENT = (
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 NewsAggregator/2.0'
)

DEFAULT_GERMAN_SOURCES = ["Heise Online", "Golem.de", "t3n", "Computerwoche", "ZDNet.de"]


# --------------------------------------------------------------------------- #
# Konfiguration
# --------------------------------------------------------------------------- #

def load_config(name: str):
    """Laedt ein Konfigurationsmodul (z.B. 'config_it')."""
    try:
        return importlib.import_module(name)
    except ImportError as e:
        raise SystemExit(f"Konfigurationsmodul '{name}.py' nicht gefunden: {e}")


def get_prefilter_keywords(config) -> List[str]:
    """
    Keyword-Vorfilter aus der Konfiguration.

    Historisch heisst die Variable je nach Config `IT_KEYWORDS_PREFILTER` oder
    `IT_KEYWORDS_IT`. Fehlt beides, wird nicht vorgefiltert (statt alles zu verwerfen).
    """
    for attr in ("IT_KEYWORDS_PREFILTER", "IT_KEYWORDS_IT"):
        keywords = getattr(config, attr, None)
        if keywords:
            return [k.lower() for k in keywords]
    logger.warning("Keine Vorfilter-Keywords in der Config gefunden — Vorfilter wird uebersprungen.")
    return []


def get_german_sources(config) -> List[str]:
    return getattr(config, "GERMAN_SOURCES", DEFAULT_GERMAN_SOURCES)


# --------------------------------------------------------------------------- #
# fetch
# --------------------------------------------------------------------------- #

def parse_entry_date(entry) -> Optional[datetime]:
    for attr in ("published_parsed", "updated_parsed"):
        parsed = getattr(entry, attr, None)
        if parsed:
            return datetime(*parsed[:6])
    return None


def clean_summary(text: str, max_length: int = 300) -> str:
    """HTML-Tags entfernen und auf max_length kuerzen (an Satz-/Wortgrenze)."""
    if not text:
        return ""
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    if len(text) <= max_length:
        return text

    cut_text = text[:max_length]
    last_space = cut_text.rfind(' ')
    last_sentence_end = max(cut_text.rfind('.'), cut_text.rfind('!'), cut_text.rfind('?'))
    if last_sentence_end > max_length * 0.7:
        return cut_text[:last_sentence_end + 1] + ".."
    if last_space != -1:
        return cut_text[:last_space] + "..."
    return cut_text + "..."


def normalize_title(title: str) -> str:
    return re.sub(r'[^\w\s]', '', title.lower()).strip()


# Zaehlpixel und Spacer-GIFs, die in Feeds als "Bild" durchgehen wuerden.
TRACKING_IMAGE_HINTS = (
    'feedburner', 'feedsportal', 'doubleclick', 'pixel', '/track', 'tracker',
    'stat?', 'analytics', 'spacer.gif', 'blank.gif', '1x1',
)

IMG_SRC_RE = re.compile(r'<img[^>]+src=["\']([^"\']+)["\']', re.IGNORECASE)


def is_usable_image(url: str) -> bool:
    """Bild-URL plausibel? Filtert Zaehlpixel, data:-URIs und Nicht-HTTP heraus."""
    if not url or not url.startswith(('http://', 'https://')):
        return False
    lowered = url.lower()
    return not any(hint in lowered for hint in TRACKING_IMAGE_HINTS)


def extract_image(entry) -> str:
    """
    Artikelbild aus einem Feed-Eintrag ziehen.

    Feeds transportieren Bilder auf mindestens fuenf Wegen und kaum zwei Quellen
    nutzen denselben — deshalb der Reihe nach durchprobieren, von der explizitesten
    Auszeichnung zur unsichersten (ein <img> irgendwo im HTML des Textes).
    Kein Bild ist ein normaler Fall, kein Fehler: dann bleibt das Feld leer.
    """
    # media:content und media:thumbnail (Media RSS) — die haeufigste explizite Auszeichnung
    for attr in ('media_content', 'media_thumbnail'):
        for item in getattr(entry, attr, None) or []:
            candidate = (item or {}).get('url', '')
            if is_usable_image(candidate):
                return candidate

    # Enclosures: <enclosure type="image/jpeg" url="..."> bzw. als link rel="enclosure"
    for item in (getattr(entry, 'enclosures', None) or []) + (getattr(entry, 'links', None) or []):
        item = item or {}
        if not (item.get('type') or '').startswith('image/'):
            continue
        candidate = item.get('href') or item.get('url') or ''
        if is_usable_image(candidate):
            return candidate

    # Letzter Ausweg: erstes <img> im Volltext oder in der Zusammenfassung
    blobs = [c.get('value', '') for c in (getattr(entry, 'content', None) or [])]
    blobs.append(getattr(entry, 'summary', '') or '')
    for blob in blobs:
        for match in IMG_SRC_RE.findall(blob):
            candidate = html.unescape(match)
            if is_usable_image(candidate):
                return candidate

    return ''


def fetch_source(url: str, source_name: str, keywords: List[str], cutoff: datetime,
                 german_sources: List[str], summary_chars: int) -> List[Dict]:
    """Einen Feed holen und die Kandidaten des Zeitfensters zurueckgeben."""
    session = requests.Session()
    session.headers.update({'User-Agent': USER_AGENT})

    try:
        response = session.get(url, timeout=15)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.warning(f"[{source_name}] Feed nicht abrufbar: {e}")
        return []

    feed = feedparser.parse(response.content)
    candidates = []

    for entry in feed.entries:
        try:
            pub_date = parse_entry_date(entry)
            if not pub_date or pub_date < cutoff:
                continue

            title = html.unescape(getattr(entry, 'title', '')).strip()
            if not title:
                continue
            summary = clean_summary(html.unescape(getattr(entry, 'summary', '')), summary_chars)

            if keywords:
                haystack = f"{title.lower()} {summary.lower()}"
                if not any(keyword in haystack for keyword in keywords):
                    continue

            candidates.append({
                'title': title,
                'summary': summary,
                'link': getattr(entry, 'link', ''),
                'published': pub_date.isoformat(),
                'source': source_name,
                'is_german_source': source_name in german_sources,
                'image': extract_image(entry),
            })
        except Exception as e:
            logger.warning(f"[{source_name}] Artikel uebersprungen: {e}")
            continue

    logger.info(f"[{source_name}] {len(candidates)} Kandidaten")
    return candidates


def dedupe(articles: List[Dict]) -> List[Dict]:
    """Duplikate ueber den normalisierten Titel entfernen, neueste zuerst."""
    articles.sort(key=lambda a: a['published'], reverse=True)
    seen = set()
    unique = []
    for article in articles:
        normalized = normalize_title(article['title'])
        if len(normalized) <= 10:
            continue
        if normalized in seen:
            continue
        seen.add(normalized)
        unique.append(article)
    return unique


def cmd_fetch(args) -> int:
    config = load_config(args.config)
    keywords = get_prefilter_keywords(config)
    german_sources = get_german_sources(config)
    cutoff = datetime.now() - timedelta(hours=args.hours)

    sources = config.NEWS_SOURCES
    if args.sources:
        wanted = {s.strip() for s in args.sources.split('|') if s.strip()}
        unknown = wanted - set(sources)
        if unknown:
            logger.warning(f"Unbekannte Quellen ignoriert: {sorted(unknown)}")
        sources = {name: url for name, url in sources.items() if name in wanted}

    all_candidates = []
    for source_name, feed_url in sources.items():
        all_candidates.extend(
            fetch_source(feed_url, source_name, keywords, cutoff, german_sources, args.summary_chars))

    unique = dedupe(all_candidates)[:args.limit]
    for index, article in enumerate(unique, 1):
        article['id'] = index

    with open(args.out, 'w', encoding='utf-8') as f:
        for article in unique:
            f.write(json.dumps(article, ensure_ascii=False) + "\n")

    summary = {
        'sources_checked': len(sources),
        'candidates_raw': len(all_candidates),
        'candidates_unique': len(unique),
        'out': args.out,
    }
    print(json.dumps(summary, ensure_ascii=False))
    return 0


# --------------------------------------------------------------------------- #
# render
# --------------------------------------------------------------------------- #

HTML_HEAD = """<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
{css}
    </style>
</head>
<body>
    <div class="header">
        <h1>🤖 {heading}</h1>
        <p>Automatisch gesammelt, Relevanz-geprüft &amp; übersetzt von Claude-Agenten • {generated} Uhr</p>
    </div>
    <div class="stats">
        <h2>📊 Statistiken</h2>
        <p><strong>{count} relevante Nachrichten</strong> aus <strong>{source_count} Quellen</strong></p>
        <p>Quellen mit relevanten Artikeln: {sources}</p>
    </div>
"""

HTML_ARTICLE = """    <div class="article">
        <h3>{index}. {title}</h3>
        <div class="article-meta">
            <span class="source-tag">{source}</span>
            <span>{published} Uhr</span>
        </div>
{image}        <div class="article-summary">{summary}</div>
        <a href="{link}" target="_blank" class="article-link" rel="noopener noreferrer">
            📖 Vollständigen Artikel lesen
        </a>
    </div>
"""

HTML_FOOT = """    <div class="footer">
        <p>Generiert von den News-Collector-Claude-Agenten (v2.0) • Alle Rechte bei den jeweiligen Originalquellen</p>
    </div>
</body>
</html>
"""


def read_jsonl(path: str) -> List[Dict]:
    articles = []
    with open(path, encoding='utf-8') as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                articles.append(json.loads(line))
            except json.JSONDecodeError as e:
                raise SystemExit(f"{path}:{line_no} ist kein gültiges JSON: {e}")
    return articles


def format_published(value: str) -> str:
    try:
        return datetime.fromisoformat(value).strftime('%d.%m.%Y %H:%M')
    except (ValueError, TypeError):
        return value or ""


def render_image(article: Dict) -> str:
    """
    Bild-Block eines Artikels — leerer String, wenn der Feed kein Bild geliefert hat.

    `onerror` blendet das Bild aus, statt ein kaputtes Symbol stehen zu lassen: die
    URLs zeigen auf fremde Server, von denen einzelne beim Oeffnen des Reports laengst
    404 liefern oder Hotlinking blockieren.
    """
    url = (article.get('image') or '').strip()
    if not is_usable_image(url):
        return ''
    return (
        '        <div class="article-image">\n'
        f'            <img src="{html.escape(url, quote=True)}" alt="" loading="lazy"\n'
        '                 referrerpolicy="no-referrer" onerror="this.parentNode.remove()">\n'
        '        </div>\n'
    )


def cmd_render(args) -> int:
    articles = read_jsonl(args.infile)
    if args.only_relevant:
        articles = [a for a in articles if a.get('relevant', True)]
    articles.sort(key=lambda a: a.get('published', ''), reverse=True)
    articles = articles[:args.limit]

    sources = sorted({a.get('source', 'Unbekannt') for a in articles})

    with open(args.out, 'w', encoding='utf-8') as f:
        f.write(HTML_HEAD.format(
            title=html.escape(args.heading),
            css=CSS,
            heading=html.escape(args.heading),
            generated=datetime.now().strftime('%d.%m.%Y %H:%M'),
            count=len(articles),
            source_count=len(sources),
            sources=html.escape(', '.join(sources)) or "—",
        ))

        if not articles:
            f.write("    <p>Keine relevanten Artikel im gewählten Zeitfenster gefunden.</p>\n")
        else:
            for index, article in enumerate(articles, 1):
                summary = article.get('summary') or "Weitere Details finden Sie im vollständigen Artikel."
                f.write(HTML_ARTICLE.format(
                    index=index,
                    title=html.escape(article.get('title', '')),
                    source=html.escape(article.get('source', '')),
                    published=format_published(article.get('published', '')),
                    image=render_image(article),
                    summary=html.escape(summary),
                    link=html.escape(article.get('link', '')),
                ))

        f.write(HTML_FOOT)

    print(json.dumps({'out': args.out, 'articles': len(articles), 'sources': len(sources)},
                     ensure_ascii=False))
    return 0


# --------------------------------------------------------------------------- #

def main() -> int:
    logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s', stream=sys.stderr)

    parser = argparse.ArgumentParser(description="Deterministische Werkzeuge fuer die News-Agenten")
    sub = parser.add_subparsers(dest='command', required=True)

    p_fetch = sub.add_parser('fetch', help='RSS holen, filtern, deduplizieren')
    p_fetch.add_argument('--config', default='config_it', help='Config-Modul ohne .py')
    p_fetch.add_argument('--out', required=True, help='Ziel-JSONL')
    p_fetch.add_argument('--hours', type=int, default=24, help='Zeitfenster in Stunden')
    p_fetch.add_argument('--limit', type=int, default=100, help='Max. Kandidaten nach Dedup')
    p_fetch.add_argument('--summary-chars', type=int, default=300, help='Max. Laenge der Zusammenfassung')
    p_fetch.add_argument('--sources', help='Nur diese Quellen, mit | getrennt (fuer Parallelisierung)')
    p_fetch.set_defaults(func=cmd_fetch)

    p_render = sub.add_parser('render', help='Finale Artikel als HTML-Report rendern')
    p_render.add_argument('--in', dest='infile', required=True, help='Quell-JSONL')
    p_render.add_argument('--out', required=True, help='Ziel-HTML')
    p_render.add_argument('--heading', default='Top IT-Nachrichten (Claude-gefiltert)')
    p_render.add_argument('--limit', type=int, default=100)
    p_render.add_argument('--only-relevant', action='store_true',
                          help='Nur Artikel mit "relevant": true rendern')
    p_render.set_defaults(func=cmd_render)

    args = parser.parse_args()
    return args.func(args)


CSS = """
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f8f9fa;
        }
        .header {
            background: linear-gradient(135deg, #007bff 0%, #6610f2 100%);
            color: white;
            padding: 30px;
            margin-bottom: 30px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        .header h1 {
            margin-bottom: 5px;
        }
        .stats {
            background: white;
            padding: 20px;
            margin-bottom: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        }
        .article {
            background: white;
            margin-bottom: 20px;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            border-left: 5px solid #007bff;
            transition: transform 0.2s ease-in-out;
        }
        .article:hover {
            transform: translateY(-3px);
        }
        .article h3 {
            margin-top: 0;
            color: #343a40;
            font-size: 1.25em;
        }
        .article-meta {
            color: #6c757d;
            font-size: 0.9em;
            margin-bottom: 10px;
        }
        .article-image {
            margin: 0 0 15px;
        }
        .article-image img {
            display: block;
            width: 100%;
            max-height: 320px;
            object-fit: cover;
            border-radius: 8px;
            background: #e9ecef;
        }
        .article-summary {
            color: #495057;
            margin-bottom: 15px;
        }
        .article-link {
            display: inline-block;
            background: #007bff;
            color: white;
            padding: 10px 18px;
            text-decoration: none;
            border-radius: 5px;
            font-size: 0.95em;
            transition: background-color 0.2s ease;
        }
        .article-link:hover {
            background: #0056b3;
        }
        .source-tag {
            background: #e9ecef;
            color: #495057;
            padding: 5px 10px;
            border-radius: 4px;
            font-size: 0.85em;
            margin-right: 10px;
        }
        .footer {
            text-align: center;
            margin-top: 50px;
            color: #6c757d;
            font-size: 0.9em;
        }
"""


if __name__ == '__main__':
    raise SystemExit(main())
