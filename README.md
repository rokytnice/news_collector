# News Collector

Sammelt Nachrichten aus RSS-Feeds, filtert sie nach Relevanz, übersetzt sie ins Deutsche und
erzeugt einen HTML-Report.

Die Arbeit erledigen **Claude-Agenten**, nicht ein Programm mit LLM-Aufrufen. Früher rief ein
Python-Skript pro Artikel ein LLM über eine REST-API auf; heute ist jede Entscheidungsstufe ein
eigener Agent, und Code gibt es nur noch für das, was deterministisch ist.

## Architektur

```
news-fetcher          RSS holen, 24h-Fenster, Keyword-Vorfilter, Dedup   -> candidates.jsonl
        ↓
news-relevance-judge  Relevanz gegen die Config-Kategorien entscheiden   -> relevant.jsonl
        ↓
news-translator       nicht-deutsche Artikel übersetzen                  -> translated.jsonl
        ↓
news-reporter         HTML-Report rendern + verifizieren                 -> it_nachrichten_*.html
```

Die Agenten liegen in [`.claude/agents/`](.claude/agents/). `news-relevance-judge` und
`news-translator` denken selbst — sie rufen **kein** LLM auf. Das spart gegenüber der alten
Lösung zwei bis drei API-Calls pro Artikel und das 6-Sekunden-Rate-Limit dazwischen.

[`feed_tools.py`](feed_tools.py) ist der deterministische Rest: HTTP, Zeitfenster,
Keyword-Vorfilter, Deduplizierung, HTML-Rendering. Ohne jede LLM-Logik.

## LLM-Policy

Claude ist das **einzige** LLM in diesem Projekt. Kein Gemini, kein OpenAI, kein DeepL,
keine Google-API — weder im Code noch in den Agenten. Auch `claude -p` aus Python heraus ist
verboten: ein Agent, der ein LLM aufruft, um zu denken, ist ein Designfehler.

## Setup

```bash
pip install requests feedparser
```

Kein API-Key nötig — die Agenten laufen in deiner Claude-Code-Session.

## Nutzung

Pipeline in Claude Code starten, z. B.:

> Sammle die IT-News der letzten 24 Stunden mit config_it.

Claude legt einen Run-Ordner unter `_work/news/<timestamp>/` an und beauftragt die vier Agenten
nacheinander. Details und Parallelisierung: [`CLAUDE.md`](CLAUDE.md).

Die Werkzeuge lassen sich auch direkt aufrufen:

```bash
# Kandidaten holen (nur RSS, keine Bewertung)
python feed_tools.py fetch --config config_it --out _work/news/candidates.jsonl --hours 24

# nur eine Teilmenge der Quellen (für parallele Fetcher)
python feed_tools.py fetch --config config_it --sources 'Heise Online|Golem.de' --out part1.jsonl

# fertige Artikel rendern
python feed_tools.py render --in translated.jsonl --out report.html --only-relevant
```

## Konfiguration

| Datei | Inhalt |
|-------|--------|
| `config_it.py` | IT-News: 164 Quellen, Vorfilter-Keywords, IT-Kategorien |
| `config_coding.py` | derzeit inhaltsgleich mit `config_politics.py` (Politik-Quellen) |
| `config_politics.py` | Politik: 126 Quellen, Keywords, Politik-Kategorien |

Pro Config: `NEWS_SOURCES`, Vorfilter-Keywords (`IT_KEYWORDS_PREFILTER` oder `IT_KEYWORDS_IT`),
`IT_CATEGORIES_FOR_LLM_PROMPT` als Relevanzmaßstab, `GERMAN_SOURCES` für die Übersetzungs-Ausnahme.

## Dateistruktur

```
.claude/agents/     Die vier Pipeline-Agenten
feed_tools.py       Deterministische Werkzeuge (fetch, render)
config_*.py         Quellen, Keywords, Kategorien
_work/news/<run>/   Zwischenstände eines Laufs (nicht in Git)
_wiki/              Architektur- und Entscheidungsdoku
```
