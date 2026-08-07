_Zuletzt aktualisiert: 2026-08-07_

# Entscheidungen

## 2026-08-07 — Gemini raus, Claude rein

`news.py` rief die Gemini-REST-API auf (`generativelanguage.googleapis.com`), Key aus
`GEMINI_API_KEY`. Vorgabe von André: nur Claude, kein anderes LLM. Zwischenschritt war ein
`subprocess`-Aufruf von `claude -p`; der ist inzwischen durch die Agenten ersetzt.

Nebenbefund: Im README stand ein echter Google-API-Key im Klartext, öffentlich auf GitHub.
Aus der Git-History entfernt (`filter-branch`, force-push, verifiziert 0 Treffer). Der Key muss
in der Google-Konsole widerrufen werden — Force-Push entfernt ihn nicht aus GitHub-Caches,
Forks oder Scraper-Datenbanken.

## 2026-08-07 — Agenten statt Programmcode

`news.py` (25 kB, eine Klasse, LLM-Aufrufe inline in der Feed-Schleife) ist gelöscht und durch
vier Agenten plus `feed_tools.py` ersetzt.

**Warum:** Die alte Struktur machte pro Artikel zwei bis drei LLM-Calls, jeder mit 6 Sekunden
Rate-Limit — bei 100 Artikeln über eine halbe Stunde reine Wartezeit. Ein Agent bewertet einen
ganzen Batch in einem Durchgang. Dazu kommt Fehler-Isolation: fällt der Übersetzer aus, sind
Fetch und Relevanzprüfung trotzdem fertig und liegen als JSONL auf der Platte.

Entspricht der Agent-Architektur-Policy (`~/.claude/memory/agent_architecture_policy.md`):
parallelisierbar, Fehler-Isolation nötig, Laufzeit > 30 s → Cloud-Agent. Der verbleibende
Python-Anteil fällt unter die Utilities-Ausnahme.

**Bewusst nicht gemacht:** RSS-Abruf und HTML-Rendering in Agenten verlagern. Beides ist
deterministisch; ein Modell, das 164 Feeds per Tool-Call durchgeht, ist langsamer und
unzuverlässiger als eine Schleife.

## 2026-08-07 — Keine Google-News-RSS-Feeds entfernt

Die `NEWS_SOURCES` enthalten `news.google.com/rss/...`-Einträge. Die sind öffentliche RSS-Feeds
ohne API-Key und von der „kein Google-API"-Vorgabe nicht betroffen — Entfernen würde nur
Quellen kosten.
