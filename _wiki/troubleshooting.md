_Zuletzt aktualisiert: 2026-08-07_

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
