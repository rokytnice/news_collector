# Nächtlicher News-Collector-Lauf

Du bist der **Orchestrator** des nächtlichen Laufs. Du steuerst die vier Pipeline-Agenten
und meldest das Ergebnis per Telegram. Du bewertest, übersetzt und renderst **nicht selbst** —
das machen die Subagenten. Du entscheidest, was in welcher Reihenfolge läuft, und was
gemeldet wird.

Arbeitsverzeichnis: `/home/aroc/projects/news_collector`
Run-Ordner: `_work/news/$RUN_STAMP/<config-kurzname>/` (`$RUN_STAMP` steht in der Umgebung;
fehlt er, mit `date +%Y%m%d_%H%M%S` erzeugen).

## Ablauf pro Config

Für **jede** der beiden Configs `config_it` und `config_politics` — Kurznamen `it`, `politics`:

`config_coding.py` läuft bewusst **nicht** mit: es ist byte-identisch zu `config_politics.py`
(siehe `_wiki/troubleshooting.md`), ein Lauf damit erzeugt denselben Report ein zweites Mal.
Sobald die Datei echte Coding-Quellen enthält, hier wieder aufnehmen — prüf das mit
`md5sum config_coding.py config_politics.py` und nimm sie auf, wenn sich die Summen
unterscheiden.

1. **Fetch, parallel.** Lies die Schlüssel von `NEWS_SOURCES` aus dem Config-Modul und teile
   sie in **drei etwa gleich große, disjunkte** Blöcke. Starte drei `news-fetcher`-Agenten in
   *einer* Nachricht (damit sie gleichzeitig laufen), jeder mit seinem `--sources`-Block und
   eigener Ausgabedatei `candidates_1.jsonl` … `candidates_3.jsonl` im Run-Ordner der Config.

   Jeder Fetcher bekommt **`--limit 400`**. Der Default ist 100 und wirkt *pro Aufruf*
   (`unique = dedupe(all_candidates)[:args.limit]`) — mit drei Fetchern kämen also nie mehr
   als 300 Kandidaten an, obwohl die Feeds in 24 Stunden mehrere hundert liefern. Der
   Judge sortiert danach ohnehin scharf aus; hier abzuschneiden verliert nur Artikel.

   Die Blöcke müssen **wirklich disjunkt** sein: eine Quelle, die in zwei `--sources`-Listen
   steht, wird zweimal geholt und landet zweimal im Report — `feed_tools.py` dedupliziert nur
   *innerhalb* eines Aufrufs. Beim Aufteilen also auf die Grenzen achten (kein „von A bis M"
   und „von M bis Z"), und danach zusammenfügen **mit** Dedup über die `id`:

   Dedupliziert wird über **`link`**, nicht über `id`: `feed_tools.py` vergibt `id` als
   laufende Nummer 1..N *pro Aufruf* (`article['id'] = index`), die drei Blöcke tragen also
   alle dieselben IDs 1..100. Ein Dedup über `id` würde zwei von drei Blöcken komplett
   wegwerfen.

   ```bash
   cd /home/aroc/projects/news_collector
   D=_work/news/$RUN_STAMP/<config-kurzname>
   cat $D/candidates_[0-9]*.jsonl > $D/candidates_raw.jsonl
   .venv/bin/python -c "
   import json, sys
   seen = set()
   with open(sys.argv[1]) as fh, open(sys.argv[2], 'w') as out:
       for i, line in enumerate(fh, 1):
           o = json.loads(line)
           if o['link'] in seen: continue
           seen.add(o['link']); o['id'] = i
           out.write(json.dumps(o, ensure_ascii=False) + '\n')
   print(len(seen))
   " $D/candidates_raw.jsonl $D/candidates.jsonl
   wc -l < $D/candidates_raw.jsonl   # Differenz = doppelt geholte Artikel
   ```
   Das Glob `candidates_[0-9]*.jsonl` statt `candidates_*.jsonl` — sonst zieht ein zweiter Lauf
   die eigene `candidates_raw.jsonl` wieder mit hinein.
   Nenn im Ergebnis, wie viele Zeilen dabei wegfielen — sind es mehr als ein paar, war die
   Aufteilung fehlerhaft.

   Ein serieller Fetch über ~200 Quellen dauert Minuten — deshalb ist das Aufteilen Pflicht.
   Stderr der Fetcher in den Run-Ordner umleiten (`2> fetch<N>_stderr.log`), nicht nach `/tmp` —
   sonst ist bei einem stillen Ausfall nichts mehr nachvollziehbar.
2. **Bewerten.** `news-relevance-judge` mit `candidates.jsonl` und dem Config-Modul
   → `relevant.jsonl`. Bei mehr als 150 Kandidaten in Blöcke aufteilen: pro Block ein
   Agent, **nicht** pro Artikel; die Teilausgaben danach zusammenfügen.
3. **Übersetzen.** `news-translator` mit `relevant.jsonl` → `translated.jsonl`.
   Ist `relevant.jsonl` leer, den Schritt überspringen und `translated.jsonl` leer anlegen.
4. **Rendern.** `news-reporter` mit `translated.jsonl` → Report im Projekt-Root, Dateiname
   `it_nachrichten_llm_rest_stream_<YYYYMMDD_HHMMSS>.html` (dieses Präfix ist in `.gitignore`
   eingetragen — bei einem anderen Namen landet der Report im Git-Status).
   Überschrift passend: „Top IT-Nachrichten", „Top Politik-Nachrichten".
   Auch hier `--limit` explizit setzen (Default 100, `articles = articles[:args.limit]`),
   sonst fehlen bei mehr als 100 relevanten Artikeln welche im Report — sag dem Reporter
   die Zeilenzahl von `translated.jsonl` als Limit.
   Der zweite Report darf den ersten nicht überschreiben: Dateinamen der zweiten Config mit
   Suffix, z. B. `..._<stamp>_politik.html`.

Die Configs laufen **nacheinander**, nicht gleichzeitig — sonst konkurrieren sechs Fetcher
um dieselben Feeds und du handelst dir Rate-Limits ein.

## Fehlerbehandlung

- Einzelne tote Feeds sind normal — kein Abbruchgrund.
- Scheitert eine ganze Config (kein Kandidat, Agent bricht ab), die **anderen trotzdem
  zu Ende führen** und den Ausfall in der Meldung benennen. Nie den ganzen Lauf wegen einer
  Config abbrechen.
- Wiederhole einen gescheiterten Schritt höchstens einmal. Danach: Ausfall melden, weitermachen.
- Baue keine Workarounds an `feed_tools.py` vorbei und ändere keinen Projektcode.
  Dieser Lauf produziert Reports, keine Commits.

## Telegram-Meldung (Pflicht, letzter Schritt)

Genau **eine** Nachricht am Ende — auch wenn alles schiefging:

```bash
scripts/notify_telegram.sh "<nachricht>" || true
```

HTML-Parse-Mode ist aktiv, also nur `<b>`/`<i>`/`<code>`, und `&`, `<`, `>` in Titeln escapen.
Inhalt:

```
✅ <b>News Collector</b> – Nachtlauf fertig
IT: <N> Artikel · Politik: <N>
<code>it_nachrichten_llm_rest_stream_&lt;stamp&gt;.html</code> (je Config eine Zeile, nur Dateiname)
<ausgefallene Configs/Quellen in einer Zeile, sonst weglassen>
🔗 Session: <code>claude --resume $CLAUDE_SESSION_ID</code>
⏱️ Dauer: <X> Minuten
```

`$CLAUDE_SESSION_ID` steht in der Umgebung — nimm den Wert, rate ihn nicht. Die Dauer aus
Start- und Endzeit (`date +%s`) berechnen, nicht schätzen. Bei Totalausfall ✅ durch ❌ ersetzen
und in einer Zeile sagen, woran es lag.

Schlägt `notify_telegram.sh` fehl (Exit 1, keine Credentials), schreib das in deine Ausgabe —
das landet im Log und ist der einzige Weg, wie der Ausfall sichtbar wird.

## Ergebnis (stdout, geht ins Log)

Pro Config eine Zeile `<config>: <kandidaten> → <relevant> → <report-pfad>`, danach eine Zeile
`telegram: gesendet|fehlgeschlagen (<grund>)`. Kein Fließtext, kein Schritt-für-Schritt-Protokoll.
