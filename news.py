#!/usr/bin/env python3
"""
IT-Nachrichten Aggregator
Sammelt und fasst IT-Coding-Nachrichten der letzten 24 Stunden zusammen,
prüft Relevanz und übersetzt mit Gemini LLM via REST API.
Streamt Ergebnisse in die HTML-Datei.
"""

import requests
import feedparser
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional, IO
import time
import html
import re
from urllib.parse import urljoin, urlparse
import logging
import os
import argparse
import importlib

# Logging konfigurieren
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - [%(funcName)s] - %(message)s')
logger = logging.getLogger(__name__)

# Konstante für die LLM-Drosselung (in Sekunden)
import config_coding


class NewsAggregator:
    def __init__(self, config_module):
        self.config = config_module
        # RSS Feeds der wichtigsten IT-Nachrichtenquellen

        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 NewsAggregator/1.1',
            'Content-Type': 'application/json'  # Wichtig für POST-Requests an Gemini API
        })

        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.gemini_model_name = self.config.GEMINI_MODEL_NAME # Oder dein bevorzugtes Modell
        self.last_llm_call_time = 0  # Zeitstempel der letzten LLM-Abfrage (Unix-Zeit)

        if not self.gemini_api_key:
            logger.warning("GEMINI_API_KEY environment variable not set. LLM features will be disabled.")
        else:
            logger.info(f"Gemini LLM ({self.gemini_model_name}) will be used via REST API.")

    def _wait_for_llm_throttle(self):
        """Wartet, um die LLM-Abfragerate zu begrenzen."""
        current_time = time.time()
        elapsed_time = current_time - self.last_llm_call_time
        if elapsed_time < self.config.LLM_RATE_LIMIT_SECONDS:
            sleep_duration = self.config.LLM_RATE_LIMIT_SECONDS - elapsed_time
            logger.debug(f"Warte {sleep_duration:.2f} Sekunden, um LLM-Rate Limit einzuhalten.")
            time.sleep(sleep_duration)
        self.last_llm_call_time = time.time()

    def _call_gemini_api(self, prompt_text: str) -> Optional[str]:
        """
        Sendet eine Anfrage an die Gemini API und gibt die Textantwort zurück.
        """
        if not self.gemini_api_key:
            logger.warning("Gemini API key not available. Skipping LLM call.")
            return None

        self._wait_for_llm_throttle()

        api_url = self.config.GEMINI_API_ENDPOINT_TEMPLATE.format(model=self.gemini_model_name, api_key=self.gemini_api_key)

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt_text}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 1,
                "topP": 1,
                "maxOutputTokens": 2048,
            }
        }
        logger.info(f"Sending request to Gemini API: {api_url}")
        logger.debug(f"Gemini API Request Payload: {json.dumps(payload, indent=2)}")

        try:
            response = self.session.post(api_url, json=payload, timeout=30)
            logger.debug(f"Gemini API Response Status Code: {response.status_code}")
            logger.debug(f"Gemini API Response Headers: {response.headers}")
            response.raise_for_status()
            response_data = response.json()
            logger.debug(f"Gemini API Response JSON: {json.dumps(response_data, indent=2)}")

            if response_data.get("candidates") and \
                    len(response_data["candidates"]) > 0 and \
                    response_data["candidates"][0].get("content") and \
                    response_data["candidates"][0]["content"].get("parts") and \
                    len(response_data["candidates"][0]["content"]["parts"]) > 0 and \
                    response_data["candidates"][0]["content"]["parts"][0].get("text"):
                generated_text = response_data["candidates"][0]["content"]["parts"][0]["text"].strip()
                logger.info("Successfully received and parsed response from Gemini API.")
                return generated_text
            else:
                logger.error(
                    f"Unerwartete Antwortstruktur von Gemini API (nach erfolgreichem Status Code): {response_data}")
                return None
        except requests.exceptions.Timeout:
            logger.error(f"Timeout bei der Anfrage an Gemini API ({api_url}).")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Fehler bei der Anfrage an Gemini API ({api_url}): {e}")
            if e.response is not None:
                logger.error(f"Gemini API Error Response Status Code: {e.response.status_code}")
                logger.error(f"Gemini API Error Response Content: {e.response.text}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Fehler beim Parsen der JSON-Antwort von Gemini API: {e}")
            if response is not None:
                logger.error(f"Gemini API Raw Response Text (JSONDecodeError): {response.text}")
            return None
        except Exception as e:
            logger.error(f"Allgemeiner Fehler beim Aufruf der Gemini API: {e}")
            return None

    def is_article_relevant_with_llm(self, title: str, summary: str) -> bool:
        """Prüft mit Gemini LLM, ob ein Artikel zu den definierten IT-Kategorien passt."""
        if not self.gemini_api_key:
            return False

        prompt_text = f"""
        Du bist ein Assistent zur Kategorisierung von Nachrichten. Deine Aufgabe ist es, zu bestimmen,
        ob der folgende Nachrichtenartikel thematisch zu EINEM der folgenden IT-Bereiche passt:
        ---
        {self.config.IT_CATEGORIES_FOR_LLM_PROMPT}
        ---

        Artikel Titel: "{title}"
        Artikel Zusammenfassung: "{summary}"

        Ist dieser Artikel relevant für diese IT-Bereiche?
        Antworte NUR mit "JA" oder "NEIN".
        """
        response_text = self._call_gemini_api(prompt_text)
        if response_text:
            decision = response_text.strip().upper()
            logger.debug(f"LLM Relevanzprüfung für '{title}': Entscheidung: {decision}")
            return decision == "JA"
        return False

    def translate_text_with_llm(self, text: str, target_lang: str = "Deutsch") -> str:
        """Übersetzt Text mit Gemini LLM."""
        if not self.gemini_api_key or not text or not text.strip():
            return text if text else ""

        prompt_text = f"""
        Übersetze den folgenden englischen Text nach {target_lang}.
        Gib NUR den übersetzten Text zurück, ohne einleitende Phrasen oder Erklärungen.

        Englischer Text:
        ---
        {text}
        ---
        Übersetzter Text:
        """
        translated_text = self._call_gemini_api(prompt_text)
        if translated_text:
            logger.debug(f"LLM Übersetzung für '{text[:30].strip()}...': '{translated_text[:30].strip()}...'")
            return translated_text
        return text

    def fetch_feed(self, url: str, source_name: str) -> List[Dict]:
        """RSS Feed abrufen, parsen, Relevanz prüfen und ggf. übersetzen."""
        try:
            logger.info(f"Lade Feed von {source_name} ({url})...")
            feed_session = requests.Session()
            feed_session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 NewsAggregator/1.1'
            })
            response = feed_session.get(url, timeout=15)
            response.raise_for_status()

            feed = feedparser.parse(response.content)
            articles = []
            cutoff_time = datetime.now() - timedelta(hours=24)

            for entry in feed.entries:
                try:
                    pub_date = None
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        pub_date = datetime(*entry.published_parsed[:6])
                    elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                        pub_date = datetime(*entry.updated_parsed[:6])

                    if not pub_date or pub_date < cutoff_time:
                        continue

                    original_title = html.unescape(entry.title).strip()
                    original_summary = html.unescape(getattr(entry, 'summary', '')).strip()

                    if not original_title:
                        logger.debug(f"Artikel von {source_name} ohne Titel übersprungen.")
                        continue

                    content_for_keyword_check = f"{original_title.lower()} {original_summary.lower()}"
                    if not any(keyword in content_for_keyword_check for keyword in self.config.IT_KEYWORDS_PREFILTER):
                        logger.debug(
                            f"Artikel '{original_title}' von {source_name} durch Keyword-Vorfilter übersprungen.")
                        continue

                    logger.info(
                        f"Artikel '{original_title}' von {source_name} hat Keyword-Vorfilter bestanden. Prüfe Relevanz mit LLM...")

                    # Hier wird der Artikel direkt verarbeitet und potenziell gestreamt,
                    # daher geben wir ihn zurück, wenn er relevant ist.
                    if self.gemini_api_key and self.is_article_relevant_with_llm(original_title, original_summary):
                        logger.info(f"Artikel '{original_title}' von {source_name} ist RELEVANT. Übersetze...")

                        is_german_source = source_name in ["Heise Online", "Golem.de", "t3n", "Computerwoche",
                                                           "ZDNet.de"]

                        translated_title = original_title
                        translated_summary = original_summary

                        if not is_german_source:
                            translated_title = self.translate_text_with_llm(original_title)
                            translated_summary = self.translate_text_with_llm(original_summary)
                        else:
                            logger.info(
                                f"Artikel '{original_title}' von deutscher Quelle '{source_name}' wird nicht übersetzt.")

                        article_data = {
                            'title': translated_title,
                            'link': entry.link,
                            'summary': translated_summary,
                            'published': pub_date,
                            'source': source_name,
                            'original_title': original_title
                        }
                        articles.append(article_data)  # Sammeln für Deduplizierung und Sortierung
                    elif self.gemini_api_key:
                        logger.info(
                            f"Artikel '{original_title}' von {source_name} ist laut LLM NICHT relevant. Übersprungen.")
                    else:
                        logger.warning(
                            f"LLM nicht verfügbar (kein API Key). Artikel '{original_title}' von {source_name} kann nicht auf Relevanz geprüft werden und wird übersprungen.")

                except Exception as e:
                    logger.warning(
                        f"Fehler beim Verarbeiten eines Artikels von {source_name} ('{entry.get('title', 'N/A')}'): {e}")
                    continue

            logger.info(
                f"{len(articles)} potenziell relevante Artikel von {source_name} für weitere Verarbeitung gefunden.")
            return articles  # Gibt alle potenziell relevanten Artikel zurück

        except requests.exceptions.Timeout:
            logger.error(f"Timeout beim Laden von {source_name} ({url}).")
            return []
        except requests.exceptions.RequestException as e:
            logger.error(f"Request-Fehler beim Laden von {source_name} ({url}): {e}")
            return []
        except Exception as e:
            logger.error(f"Allgemeiner Fehler beim Laden von {source_name} ({url}): {e}")
            return []

    def clean_summary(self, text: str, max_length: int = 300) -> str:
        """HTML Tags entfernen und Text kürzen"""
        if not text:
            return ""
        text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        if len(text) > max_length:
            cut_text = text[:max_length]
            last_space = cut_text.rfind(' ')
            last_sentence_end = max(cut_text.rfind('.'), cut_text.rfind('!'), cut_text.rfind('?'))

            if last_sentence_end > max_length * 0.7:
                text = cut_text[:last_sentence_end + 1] + ".."
            elif last_space != -1:
                text = cut_text[:last_space] + "..."
            else:
                text = cut_text + "..."
        return text

    def get_html_header(self) -> str:
        """Generiert den HTML-Header und den Anfang des Body-Tags."""
        return f"""
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IT-Nachrichten der letzten 24 Stunden (LLM-gefiltert & übersetzt)</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f8f9fa;
        }}
        .header {{
            background: linear-gradient(135deg, #007bff 0%, #6610f2 100%);
            color: white;
            padding: 30px;
            margin-bottom: 30px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        .header h1 {{
            margin-bottom: 5px;
        }}
        .stats {{
            background: white;
            padding: 20px;
            margin-bottom: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        }}
        .article {{
            background: white;
            margin-bottom: 20px;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            border-left: 5px solid #007bff;
            transition: transform 0.2s ease-in-out;
        }}
        .article:hover {{
            transform: translateY(-3px);
        }}
        .article h3 {{
            margin-top: 0;
            color: #343a40;
            font-size: 1.25em;
        }}
        .article-meta {{
            color: #6c757d;
            font-size: 0.9em;
            margin-bottom: 10px;
        }}
        .article-summary {{
            color: #495057;
            margin-bottom: 15px;
        }}
        .article-link {{
            display: inline-block;
            background: #007bff;
            color: white;
            padding: 10px 18px;
            text-decoration: none;
            border-radius: 5px;
            font-size: 0.95em;
            transition: background-color 0.2s ease;
        }}
        .article-link:hover {{
            background: #0056b3;
        }}
        .source-tag {{
            background: #e9ecef;
            color: #495057;
            padding: 5px 10px;
            border-radius: 4px;
            font-size: 0.85em;
            margin-right: 10px;
        }}
        .footer {{
            text-align: center;
            margin-top: 50px;
            color: #6c757d;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🤖 Top IT-Nachrichten (LLM-gefiltert)</h1>
        <p>Automatisch gesammelt, Relevanz-geprüft & übersetzt • {datetime.now().strftime('%d.%m.%Y %H:%M')} Uhr</p>
    </div>
    <!-- Platzhalter für Statistiken, wird später gefüllt oder am Ende -->
    <div class="stats" id="stats-placeholder">
        <h2>📊 Statistiken</h2>
        <p>Artikel werden geladen...</p>
    </div>
"""

    def get_html_footer(self) -> str:
        """Generiert den HTML-Footer."""
        return """
    <div class="footer">
        <p>Generiert mit IT-Nachrichten Aggregator (v1.3 mit Gemini REST API Streaming) • Alle Rechte bei den jeweiligen Originalquellen</p>
    </div>
</body>
</html>
"""

    def format_article_as_html(self, article: Dict, index: int) -> str:
        """Formatiert einen einzelnen Artikel als HTML-Block."""
        summary = self.clean_summary(article['summary'], 300)
        if not summary and article['title']:
            summary = "Weitere Details finden Sie im vollständigen Artikel."
        pub_date = article['published'].strftime('%d.%m.%Y %H:%M')

        return f"""
    <div class="article">
        <h3>{index}. {html.escape(article['title'])}</h3>
        <div class="article-meta">
            <span class="source-tag">{html.escape(article['source'])}</span>
            <span>{pub_date} Uhr</span>
        </div>
        <div class="article-summary">{html.escape(summary)}</div>
        <a href="{html.escape(article['link'])}" target="_blank" class="article-link" rel="noopener noreferrer">
            📖 Vollständigen Artikel lesen
        </a>
    </div>
"""

    def stream_news_to_file(self, filename: str = None):
        """Sammelt Nachrichten und streamt sie direkt in die HTML-Datei."""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"it_nachrichten_llm_rest_stream_{timestamp}.html"

        processed_articles_count = 0
        sources_with_articles = set()

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.get_html_header())
                f.flush()  # Sicherstellen, dass der Header geschrieben wird

                # Zuerst alle potenziellen Artikel sammeln, um Deduplizierung und Sortierung zu ermöglichen
                # Dies ist ein Kompromiss zum reinen Streaming pro Feed-Eintrag
                all_potential_articles = []
                for source_name, feed_url in self.config.NEWS_SOURCES.items():
                    # Die fetch_feed Methode prüft bereits Relevanz und übersetzt
                    articles_from_source = self.fetch_feed(feed_url, source_name)
                    all_potential_articles.extend(articles_from_source)
                    time.sleep(0.2)  # Kleine Pause zwischen den Feeds

                # Sortieren nach Datum
                all_potential_articles.sort(key=lambda x: x['published'], reverse=True)

                # Deduplizieren
                unique_articles_to_stream = []
                seen_original_titles_normalized = set()
                for article_data in all_potential_articles:
                    title_to_check = article_data.get('original_title', article_data['title'])
                    normalized_title = re.sub(r'[^\w\s]', '', title_to_check.lower()).strip()
                    if normalized_title not in seen_original_titles_normalized and len(normalized_title) > 10:
                        seen_original_titles_normalized.add(normalized_title)
                        unique_articles_to_stream.append(article_data)
                    elif len(normalized_title) <= 10:
                        logger.debug(f"Deduplizierung: Kurzen Titel übersprungen: '{normalized_title}'")
                    else:
                        logger.info(f"Deduplizierung: Duplikat entfernt: '{title_to_check}'")

                logger.info(f"{len(unique_articles_to_stream)} einzigartige Artikel zum Streamen vorbereitet.")

                # Begrenzen auf die Top 100 nach Deduplizierung und Sortierung
                articles_to_output = unique_articles_to_stream[:100]

                if not articles_to_output:
                    f.write(
                        "<p>Keine relevanten Artikel in den letzten 24 Stunden gefunden oder LLM nicht verfügbar.</p>\n")
                else:
                    for i, article_data in enumerate(articles_to_output, 1):
                        article_html = self.format_article_as_html(article_data, i)
                        f.write(article_html)
                        f.flush()  # Artikel sofort schreiben
                        processed_articles_count += 1
                        sources_with_articles.add(article_data['source'])
                        logger.info(f"Artikel {i} ('{article_data['title'][:30]}...') in Datei gestreamt.")

                # Statistiken am Ende aktualisieren (einfache Methode, erfordert JS im Browser oder Neuschreiben)
                # Für eine reine Server-Lösung müsste man die Datei temporär halten und den Platzhalter ersetzen.
                # Hier eine vereinfachte Version, die den Footer schreibt.
                # Eine robustere Statistikaktualisierung wäre komplexer.
                stats_html = f"""
    <script>
        document.getElementById('stats-placeholder').innerHTML = `
            <h2>📊 Statistiken</h2>
            <p><strong>{processed_articles_count} relevante IT-Nachrichten</strong> aus <strong>{len(sources_with_articles)} verschiedenen Quellen</strong></p>
            <p>Geprüfte Quellen: {', '.join(sorted(list(self.config.NEWS_SOURCES.keys())))}</p>
            <p>Quellen mit relevanten Artikeln: {', '.join(sorted(list(sources_with_articles)))}</p>
        `;
    </script>
"""
                f.write(stats_html)
                f.write(self.get_html_footer())

            logger.info(f"Zusammenfassung erfolgreich gestreamt und gespeichert: {filename}")
            return filename, processed_articles_count, len(sources_with_articles)

        except IOError as e:
            logger.error(f"Fehler beim Schreiben der Streaming-Datei {filename}: {e}")
            return None, 0, 0
        except Exception as e:
            logger.error(f"Unerwarteter Fehler beim Streamen der Nachrichten: {e}")
            return None, 0, 0


def main():
    """Hauptfunktion"""
    logger.info("Starte IT-Nachrichten Aggregator mit Gemini REST API Streaming...")

    parser = argparse.ArgumentParser(description="IT-Nachrichten Aggregator")
    parser.add_argument(
        "--config",
        type=str,
        default="config",
        help="Name des Konfigurationsmoduls (ohne .py Endung). Standard: config"
    )
    args = parser.parse_args()

    try:
        config_module = importlib.import_module(args.config)
    except ImportError:
        logger.error(f"Konfigurationsmodul '{args.config}.py' nicht gefunden.")
        return

    aggregator = NewsAggregator(config_module)

    if not aggregator.gemini_api_key:
        logger.warning(
            "Kein GEMINI_API_KEY gefunden. LLM-Funktionalität ist deaktiviert.")

    logger.info("Sammle und streame Nachrichten (inkl. LLM-Prüfung und Übersetzung via REST API)...")

    # Die Logik zum Sammeln und Generieren der gesamten HTML ist jetzt in stream_news_to_file
    filename, num_articles, num_sources = aggregator.stream_news_to_file()

    if not filename:
        logger.error("Konnte die Zusammenfassung nicht erstellen oder streamen.")
        # Erstelle eine leere Datei, falls noch nicht geschehen
        if not os.path.exists("it_nachrichten_llm_rest_stream_leer.html"):
            try:
                with open("it_nachrichten_llm_rest_stream_leer.html", 'w', encoding='utf-8') as f_empty:
                    f_empty.write(aggregator.get_html_header())
                    f_empty.write("<p>Fehler beim Laden der Artikel oder keine relevanten Artikel gefunden.</p>")
                    f_empty.write(aggregator.get_html_footer())
                print(
                    "\nEine leere Zusammenfassung (Fehlerfall) wurde erstellt: it_nachrichten_llm_rest_stream_leer.html")
            except Exception as e_empty:
                print(f"Konnte auch keine leere Fehlerdatei erstellen: {e_empty}")
            return

    if num_articles == 0:
        print(f"\nKeine relevanten Artikel gefunden. Die Datei '{filename}' enthält eine entsprechende Meldung.")
    else:
        print("\n" + "=" * 60)
        print("IT-NACHRICHTEN ZUSAMMENFASSUNG (GESTREAMT VIA REST)")
        print("=" * 60)
        print(f"Anzahl relevanter Artikel: {num_articles}")
        print(f"Quellen mit relevanten Artikeln: {num_sources}")
        print(f"Gespeichert und gestreamt in: {filename}")
        print("=" * 60)

        # Die Vorschau ist hier weniger sinnvoll, da die Datei bereits geschrieben wurde.
        # Man könnte die ersten paar Zeilen der Datei lesen, aber das ist optional.


if __name__ == "__main__":
    main()