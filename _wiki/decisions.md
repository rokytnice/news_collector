_Zuletzt aktualisiert: 2026-08-08_

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

## 2026-08-08 — Nachtlauf lokal per Cron, nicht als Cloud-Routine

Der tägliche Lauf startet um 05:00 über `crontab` → `scripts/nightly.sh` → `claude -p` mit
`scripts/nightly_prompt.md`.

**Warum nicht als Cloud-Routine** (`/schedule`, claude.ai/code/routines), obwohl das der
naheliegende Weg für einen geplanten Agenten wäre: die Pipeline hängt an drei lokalen Dingen,
die es in der Cloud-Sandbox nicht gibt — dem `.venv` mit `feedparser`, den Reports im lokalen
Projekt-Root (die André im Browser öffnet) und den Telegram-Credentials in
`/run/user/1000/secrets.env`. Ein Cloud-Agent würde in einem frischen Checkout rendern und
das Ergebnis mit dem Container wegwerfen.

**Warum trotzdem ein Agent und kein Shell-Skript mit vier `claude`-Aufrufen:** die Entscheidungen
im Lauf sind echt — wie die ~200 Quellen auf drei Fetcher aufgeteilt werden, ob ein
Config-Ausfall den Rest stoppt, was in die Meldung gehört. Das Skript stellt nur die Umgebung
her; alles Urteilende macht der Orchestrator.

Das kollidiert **nicht** mit der Regel „kein `claude -p`" aus `CLAUDE.md`. Verboten ist, dass
Projektcode ein LLM als Subprozess zum Denken aufruft (`news.py` machte das pro Artikel).
Hier startet Cron den Agenten als oberste Ebene — der Agent ruft kein LLM auf, er ist eins.

## 2026-08-08 — `config_coding` läuft im Nachtlauf nicht mit

Solange `config_coding.py` byte-identisch zu `config_politics.py` ist, erzeugt ein Lauf damit
denselben Report ein zweites Mal. Der Orchestrator prüft das per `md5sum` und nimmt die Config
wieder auf, sobald sie sich unterscheidet.

## 2026-08-08 — Enge Kategorienliste in `config_it`

`IT_CATEGORIES_FOR_LLM_PROMPT` in `config_it.py` ist von acht breiten IT-Themen auf neun
konkrete Interessen umgestellt: KI-Forschung, KI/Robotik, KI-Codegenerierung, Agentic Coding,
Agentic Engineering, Java, Broadcom/Spring, Fake Shops und Online-Betrug, Software-Forschung.

**Warum das eine echte Verschärfung ist:** vorher war „Cloud und Infrastruktur" oder
„Tech-Branche" eine Kategorie — damit passte fast jede Meldung. Jetzt fällt ein
Smartphone-Launch oder eine beliebige CVE-Meldung explizit raus. Das steht auch so im
Kategorientext, weil der Judge sonst aus Gewohnheit breit auslegt.

**Zusammenspiel mit dem Vorfilter:** `IT_KEYWORDS_IT` wurde im Gegenzug *erweitert*, nicht
verengt (jetzt 106 Begriffe: llm, agentic, mcp, jdk, spring, fake shop, …). Die beiden
Mechanismen arbeiten gegenläufig und das ist Absicht — der Keyword-Vorfilter soll großzügig
durchlassen, die Auswahl trifft der Judge, der die Kategorien kennt. Ein Artikel, den der
Vorfilter verwirft, wird nie bewertet; ein Begriff, der hier fehlt, kostet also Artikel.
