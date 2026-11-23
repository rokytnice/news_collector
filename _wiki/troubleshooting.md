_Zuletzt aktualisiert: 2026-09-02_

# Troubleshooting

## Report ist leer, obwohl Feeds antworten

**Ursache 1 — Vorfilter greift zu hart.** Der Keyword-Vorfilter heißt je nach Config
`IT_KEYWORDS_PREFILTER` (coding, politics) oder `IT_KEYWORDS_IT` (it). Bis 2026-08-07 suchte
`news.py` ausschließlich nach `IT_KEYWORDS_PREFILTER` — mit `config_it` fiel dadurch **jeder**
Artikel durch und jeder Lauf lieferte 0 Treffer, ohne Fehlermeldung. `feed_tools.py` akzeptiert
jetzt beide Namen und filtert lieber gar nicht vor, als alles zu verwerfen.

**Ursache 2 — Zeitfenster.** `--hours 24` bezieht sich auf `published`/`updated` aus dem Feed.
Feeds ohne Datumsfeld liefern nie Kandidaten.

Diagnose:
```bash
python feed_tools.py fetch --config config_it --sources 'Heise Online' --out /tmp/t.jsonl --hours 72
wc -l /tmp/t.jsonl
```

## Tote Feeds

Von den ~164 Quellen antwortet ein Teil dauerhaft mit 404 oder TLS-Fehlern
(z. B. `umbrellatech.co`). Das ist erwartet: `feed_tools.py` loggt sie auf stderr und macht
weiter. Der `news-fetcher` sammelt sie und nennt sie im Ergebnis — kein Abbruchgrund.

## config_coding ist Politik

`config_coding.py` und `config_politics.py` sind byte-identisch, beide mit Politik-Quellen und
Politik-Kategorien. Wer „Coding-News" erwartet, bekommt Bundestagsmeldungen. Noch nicht
korrigiert, weil die passenden Coding-Quellen inhaltlich festgelegt werden müssen.

## Ein Agent ruft ein LLM auf

Ist ein Bug, kein Feature. `claude -p`, `curl` gegen eine LLM-API oder ein SDK-Import in einem
der Pipeline-Agenten gehört entfernt — der Agent ist selbst das Modell. Siehe
[decisions.md](decisions.md).

## Nachtlauf lief nicht / keine Telegram-Meldung

Reihenfolge beim Nachsehen:

1. `ls -t _logs/nightly_*.log | head -1` — fehlt ein Log für die Nacht, ist der Cronjob gar nicht
   gestartet (`crontab -l | grep news_collector`, Rechner aus, `nightly.sh` nicht ausführbar).
2. Log vorhanden, endet mit `=== exit 124 ===` → `timeout 90m` hat zugeschlagen.
   `exit 1` → Claude selbst abgebrochen; in beiden Fällen sollte der Notruf gekommen sein.
3. Log endet mit `telegram: fehlgeschlagen` oder `keine Telegram-Credentials gefunden`:
   `/run/user/1000/secrets.env` fehlt. Die Datei liegt im tmpfs und ist nach jedem Reboot weg —
   einmal `~/.claude/unlock_secrets.sh` ausführen. Unter Cron ist der GPG-Agent gesperrt,
   `pass show` kann nicht einspringen.
4. Lauf komplett nachvollziehen: `claude --resume <session-id>` (ID steht in Zeile 2 des Logs).

## Nur 300 Kandidaten, obwohl die Feeds mehr liefern

`feed_tools.py fetch --limit` wirkt **pro Aufruf** (`unique = dedupe(all_candidates)[:limit]`),
Default 100. Bei drei parallelen Fetchern sind das 300 — im Lauf vom 2026-08-08 standen dem
roh 472 (IT) bzw. 809 (Politik) Artikel gegenüber. Der Nachtlauf-Prompt setzt deshalb
`--limit 400` je Fetcher. Dasselbe gilt für `render --limit`: über 100 relevante Artikel
fehlen sonst still im Report.

## Dedup nach dem Zusammenführen: über `link`, nie über `id`

`feed_tools.py` vergibt `id` als laufende Nummer 1..N **pro Aufruf** (`article['id'] = index`).
Nach `cat candidates_1..3.jsonl` tragen alle drei Blöcke die IDs 1..100 — ein Dedup über `id`
wirft zwei Drittel der Kandidaten weg und sieht dabei aus wie erfolgreiche Deduplizierung
(300 → 100). Richtig ist `link`; die `id` danach neu durchnummerieren.

## `is_german_source` ist bei vielen deutschen Quellen `false`

Im Lauf vom 2026-09-02 meldeten alle fünf Politik-Übersetzer dasselbe: Artikel von Tagesschau,
ZDF heute, FAZ, SZ, n-tv, ORF, SRF, Spiegel und den Google-News-DE-Feeds kamen mit
`is_german_source: false` an, obwohl Titel und Zusammenfassung bereits deutsch waren
(allein in Block 01: 44 von 135). `get_german_sources()` erkennt sie also nicht.

Folge ist keine falsche Ausgabe, aber unnötige Arbeit: der Übersetzer muss jede Zeile selbst
auf Sprache prüfen, statt sich auf das Flag zu verlassen. Wer den Übersetzer-Agenten anpasst,
darf `is_german_source: false` deshalb **nicht** als „ist fremdsprachig" lesen — sonst werden
deutsche Texte ein zweites Mal durch die Übersetzung gedreht.

## Politik-Fetch stößt ans `--limit`

Ebenfalls 2026-09-02: Politik-Block 2 lieferte roh 452 Artikel und wurde bei `--limit 400`
gekappt (~52 verloren). Die drei Blöcke sind unterschiedlich ergiebig — 342 / 400 / 286.
Wenn eine Blockzahl exakt dem Limit entspricht, wurde gekappt; dann für `config_politics`
das Limit anheben oder in vier statt drei Blöcke teilen.
