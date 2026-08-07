_Zuletzt aktualisiert: 2026-08-07_

# Architektur

## Aufteilung

Die Leitlinie: **Entscheidungen gehören in Agenten, I/O und Formatierung in Code.**

| Stufe | Wer | Warum |
|-------|-----|-------|
| RSS holen, 24h-Fenster, Keyword-Vorfilter, Dedup | `feed_tools.py fetch` | rein deterministisch, ~200 HTTP-Requests |
| Relevanz entscheiden | Agent `news-relevance-judge` | Urteilsfrage, kein Regelwerk |
| Übersetzen | Agent `news-translator` | Sprachaufgabe |
| HTML rendern | `feed_tools.py render` | Template-Anwendung, kein Urteil |
| Orchestrierung, Run-Ordner, Parallelisierung | Hauptsession nach `CLAUDE.md` | — |

Die Agenten in `.claude/agents/` haben jeweils nur `Bash`, `Read`, `Write` — bewusst kein
Browser, kein Netzzugriff außer über `feed_tools.py`.

## Datenfluss

```
_work/news/<YYYYMMDD_HHMMSS>/
  candidates.jsonl    news-fetcher          id,title,summary,link,published,source,is_german_source
  relevant.jsonl      news-relevance-judge  + relevant:true, reason
  translated.jsonl    news-translator       + original_title (bei Übersetzung)
../it_nachrichten_*.html                    news-reporter
```

Jede Stufe schreibt eine **neue** Datei und fasst die Eingabe nicht an. Dadurch ist jeder
Schritt einzeln wiederholbar, ohne die Pipeline von vorn zu starten.

## Parallelisierung

Nur der Fetch lohnt sich parallel: mehrere `news-fetcher` mit disjunkten `--sources`-Listen und
je eigener Ausgabedatei, danach `cat` zu einer Datei. Bei 126–164 Quellen dauert ein serieller
Fetch mehrere Minuten, ein Vierer-Fan-out entsprechend weniger.

Judge und Translator bei großen Mengen in Blöcken (~100–150 Artikel), aber **ein Agent pro
Block, nicht pro Artikel** — sonst ist man wieder bei der alten Ein-Call-pro-Artikel-Ökonomie.

## Kein LLM im Code

`feed_tools.py` enthält keine LLM-Logik und darf keine bekommen. Ein Agent, der `claude -p`
als Subprozess startet, ist ebenfalls falsch — er *ist* das Modell. Siehe
[decisions.md](decisions.md).
