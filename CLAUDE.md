# News Collector — Projektregeln

## LLM-Policy (hart)

**Claude ist das einzige LLM in diesem Projekt.** Kein Gemini, kein OpenAI, kein DeepL,
keine Google-API — weder im Code noch in Agenten, weder per SDK noch per `curl`.

Die Bewertung und Übersetzung macht **der Agent selbst**, nicht ein Subprozess:
`claude -p` aus Python heraus aufzurufen ist ebenfalls verboten. Ein Agent, der ein LLM
aufruft, um zu denken, ist ein Fehler im Design — er *ist* das LLM.

## Architektur

Die Pipeline besteht aus vier Agenten in `.claude/agents/` und einem deterministischen
Werkzeugmodul. Die Trennlinie: **alles, was eine Entscheidung ist, gehört in einen Agenten;
alles, was nur I/O und Formatierung ist, bleibt Code.**

```
news-fetcher          RSS holen, 24h-Fenster, Keyword-Vorfilter, Dedup   -> candidates.jsonl
        ↓
news-relevance-judge  Relevanz gegen die Config-Kategorien entscheiden   -> relevant.jsonl
        ↓
news-translator       nicht-deutsche Artikel übersetzen                  -> translated.jsonl
        ↓
news-reporter         HTML-Report rendern + verifizieren                 -> it_nachrichten_*.html
```

`feed_tools.py` ist der Python-Anteil (Ausnahme „Utilities" der Agent-Architektur-Policy):
`fetch` und `render`, ohne jede LLM-Logik.

## Pipeline starten

Ein Run bekommt einen eigenen Ordner unter `_work/news/<YYYYMMDD_HHMMSS>/`.
Die vier Agenten nacheinander mit dem Run-Ordner und dem Config-Modul beauftragen —
jeder gibt den Pfad zurück, den der nächste als Eingabe braucht.

**Parallelisierung:** Nur der `news-fetcher` lohnt sich parallel — mehrere Instanzen mit
disjunkten `--sources`-Listen und je eigener Ausgabedatei (`candidates_1.jsonl`, …),
danach `cat` zu einer Datei. Die Configs haben ~200 Quellen; ein serieller Fetch dauert
mehrere Minuten. `news-relevance-judge` und `news-translator` bei großen Mengen ebenfalls
in Blöcke aufteilen, aber pro Block ein Agent, nicht pro Artikel.

## Nachtlauf

`scripts/nightly.sh` läuft per Cron täglich um 05:00 und startet `claude -p` mit
`scripts/nightly_prompt.md`. Dieser Claude-Orchestrator steuert die vier Agenten für alle
drei Configs nacheinander und meldet am Ende per `scripts/notify_telegram.sh`.

Die Trennung ist Absicht: das Shell-Skript stellt nur die Umgebung her (PATH, Secrets aus
`/run/user/<uid>/secrets.env`, Session-ID, Log) und sendet einen Notruf, falls Claude gar
nicht hochkommt. Jede Entscheidung — Quellenaufteilung, Umgang mit Ausfällen, Inhalt der
Meldung — trifft der Orchestrator. Kein `claude -p` aus Python; hier startet die Shell den
Agenten, statt dass Code ein LLM zum Denken aufruft.

Logs: `_logs/nightly_<stamp>.log` (nicht in Git). Nachvollziehen mit
`claude --resume <session-id>` — die ID steht in der ersten Logzeile und in der Telegram-Meldung.

## Configs

`config_it.py`, `config_coding.py`, `config_politics.py` — je `NEWS_SOURCES`,
Vorfilter-Keywords, `IT_CATEGORIES_FOR_LLM_PROMPT`. Der Keyword-Vorfilter heißt historisch
je nach Datei `IT_KEYWORDS_PREFILTER` oder `IT_KEYWORDS_IT`; `feed_tools.py` akzeptiert beide
und filtert lieber gar nicht vor, als alles zu verwerfen.

`CLAUDE_*`-Variablen in den Configs sind Altlast aus der CLI-Zeit und werden von der
Agenten-Pipeline nicht mehr gelesen.

## Ausgaben

- Zwischenstände: `_work/news/<run>/` (nicht in Git)
- Reports: `it_nachrichten_*.html` im Projekt-Root (nicht in Git, siehe `.gitignore`)

## Wissen festhalten — gilt auch für die Agenten dieses Projekts

Nach jedem substantiellen Lauf prüfen: Architektur-Entscheidung getroffen? Fehler analysiert und
behoben? Nicht-triviales Feature? Gotcha entdeckt, der künftige Läufe Stunden kostet? → als
thematische Datei nach `_wiki/` (Projekt-Root, wird committet; jede Datei beginnt mit
`_Zuletzt aktualisiert: YYYY-MM-DD_`). **Nicht** für Typos, Umbenennungen oder Dinge, für die der
Code selbst spricht — und **nicht** für Lauf-Ergebnisse, die gehören nach `_reports/`.

Das ist die globale Regel §6; sie steht hier, weil Agenten die Projekt-`CLAUDE.md` mitlesen, ihre
eigene Definition unter `.claude/agents/` sie aber nicht erwähnt.
