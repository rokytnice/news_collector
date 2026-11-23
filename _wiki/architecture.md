_Zuletzt aktualisiert: 2026-08-08_

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

## Nachtlauf

```
cron 05:00 -> scripts/nightly.sh -> claude -p (scripts/nightly_prompt.md)
                                        |
                                        +-- pro Config: fetcher x3 -> judge -> translator -> reporter
                                        +-- scripts/notify_telegram.sh
```

`nightly.sh` enthält bewusst keine Logik über den Lauf: PATH für Cron setzen, Secrets aus
`/run/user/<uid>/secrets.env` laden, `RUN_STAMP` und `CLAUDE_SESSION_ID` vergeben, Log anlegen,
`timeout 90m` und ein Notruf per Telegram, falls Claude selbst nicht durchkommt. Alles andere
entscheidet der Orchestrator.

Die Session-ID wird **vorab** im Skript erzeugt und per `--session-id` übergeben, damit die
Telegram-Meldung ein funktionierendes `claude --resume <id>` enthalten kann. Ein Agent kennt
seine eigene Session-ID sonst nicht.

## Artikelbilder

`fetch` legt pro Kandidat ein Feld `image` an (leer, wenn der Feed keins liefert),
`render` macht daraus einen `.article-image`-Block zwischen Meta-Zeile und Zusammenfassung.

`extract_image()` probiert vier Wege in dieser Reihenfolge durch, weil kaum zwei Feeds
denselben nutzen: `media:content`, `media:thumbnail`, `<enclosure type="image/*">` bzw.
`link rel="enclosure"`, und als letzter Ausweg das erste `<img>` im Volltext oder in der
Zusammenfassung. Zählpixel und Spacer-GIFs fliegen über `TRACKING_IMAGE_HINTS` raus —
sonst landen Feedburner-Tracker als „Artikelbild" im Report.

Kein Bild ist der Normalfall, kein Fehler: im Test hatten 42 von 60 Artikeln eins,
TechRepublic liefert grundsätzlich keine (weder Media-RSS noch `<img>` im Text).

Die Bilder werden **nicht** heruntergeladen, sondern von der Originalquelle verlinkt
(`referrerpolicy="no-referrer"`, `loading="lazy"`). Der Report bleibt dadurch klein, aber
ein Bild kann später verschwinden; `onerror` entfernt den Block dann, statt ein kaputtes
Symbol stehen zu lassen. Wer den Report offline lesbar braucht, müsste die Bilder spiegeln —
bewusst nicht gemacht.

Judge und Translator müssen `image` unverändert durchreichen; das steht in beiden
Agent-Dateien. Wer JSONL-Zeilen neu zusammensetzt statt sie durchzureichen, verliert es.
