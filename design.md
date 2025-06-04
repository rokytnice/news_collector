# Anforderungsdokument: IT-Nachrichten Aggregator

## 1. Ziel des Programms

Das Programm soll als IT-Nachrichten-Aggregator dienen. Es sammelt Nachrichtenartikel aus verschiedenen vordefinierten RSS-Feeds, filtert diese nach Relevanz für IT-Themen, übersetzt sie gegebenenfalls ins Deutsche und stellt die Ergebnisse in einer übersichtlichen HTML-Datei dar. Die Verarbeitung soll Aspekte des Streamings berücksichtigen, um Ergebnisse frühzeitig sichtbar zu machen.

## 2. Kernfunktionalitäten

### 2.1. Nachrichtenbeschaffung:
*   Das Programm muss in der Lage sein, RSS-Feeds von einer konfigurierbaren Liste von Nachrichtenquellen abzurufen.
*   Die Liste der Nachrichtenquellen (Name und RSS-Feed-URL) soll leicht erweiterbar sein.
*   Es soll Artikel der letzten 24 Stunden berücksichtigen.
*   Fehler beim Abrufen einzelner Feeds (z.B. Timeout, HTTP-Fehler) dürfen den Gesamtprozess nicht blockieren; fehlerhafte Feeds sollen übersprungen und geloggt werden.

### 2.2. Artikel-Vorfilterung:
*   Artikel sollen anhand einer konfigurierbaren Liste von IT-spezifischen Keywords vorab gefiltert werden. Artikel, die keines dieser Keywords im Titel oder in der Zusammenfassung enthalten, sollen verworfen werden.

### 2.3. Relevanzprüfung mittels LLM (Large Language Model):
*   Für Artikel, die den Keyword-Vorfilter passieren, soll eine detailliertere Relevanzprüfung mittels eines LLM (z.B. Google Gemini) durchgeführt werden.
*   Das LLM soll anhand eines definierten Prompts prüfen, ob der Artikel thematisch zu einer vordefinierten Liste von IT-Kategorien passt.
*   Die Kommunikation mit dem LLM soll über dessen REST API erfolgen.
*   Der API-Key für das LLM soll aus einer Umgebungsvariable (`GEMINI_API_KEY`) gelesen werden.
*   Das zu verwendende LLM-Modell (z.B. "gemini-1.5-flash") soll konfigurierbar sein.
*   Die Antwort des LLM zur Relevanz ("JA"/"NEIN") soll ausgewertet werden. Nur als relevant eingestufte Artikel werden weiterverarbeitet.

### 2.4. Übersetzung mittels LLM:
*   Relevante Artikel, die nicht aus deutschsprachigen Quellen stammen, sollen mithilfe des LLM ins Deutsche übersetzt werden (Titel und Zusammenfassung).
*   Der Prompt für die Übersetzung soll sicherstellen, dass nur der übersetzte Text ohne zusätzliche Phrasen zurückgegeben wird.
*   Deutschsprachige Quellen sollen von der Übersetzung ausgenommen werden.

### 2.5. LLM API-Drosselung (Rate Limiting):
*   Um API-Limits des LLM-Anbieters nicht zu überschreiten, muss eine Drosselungsfunktion implementiert werden. Es soll sichergestellt werden, dass maximal alle X Sekunden (konfigurierbar, z.B. 6 Sekunden) eine Anfrage an die LLM-API gesendet wird.

### 2.6. Deduplizierung:
*   Nachdem alle potenziell relevanten Artikel gesammelt und verarbeitet wurden, sollen Duplikate entfernt werden. Die Deduplizierung soll primär auf Basis des normalisierten Originaltitels erfolgen.

### 2.7. HTML-Ausgabe und Streaming:
*   Die aggregierten, gefilterten, übersetzten und deduplizierten Nachrichten sollen in einer einzelnen HTML-Datei ausgegeben werden.
*   Die HTML-Datei soll einen ansprechenden und lesbaren Aufbau haben (Header, Artikelauflistung, Footer).
*   Jeder Artikel soll mit Titel, Quelle, Veröffentlichungsdatum, einer gekürzten Zusammenfassung und einem Link zum Originalartikel dargestellt werden.
*   Das Programm soll die Ergebnisse "streamen", d.h. der HTML-Header wird zu Beginn geschrieben, und jeder verarbeitete (relevante, übersetzte, deduplizierte) Artikel wird unmittelbar danach in die Datei geschrieben und geflusht.
*   Am Anfang der HTML-Datei soll ein Platzhalter für Statistiken (Anzahl Artikel, Quellen) vorgesehen werden. Diese Statistiken sollen am Ende der Verarbeitung (nachdem alle Artikel geschrieben wurden) mittels eines clientseitigen JavaScript-Snippets in den Platzhalter eingefügt werden.
*   Der Dateiname der HTML-Ausgabe soll einen Zeitstempel enthalten, um frühere Läufe nicht zu überschreiben.
*   Im Falle, dass keine relevanten Artikel gefunden werden oder ein schwerwiegender Fehler auftritt, soll eine HTML-Datei mit einer entsprechenden Meldung erstellt werden.

### 2.8. Zusammenfassungsbereinigung:
*   Die Artikelzusammenfassungen sollen von HTML-Tags bereinigt und auf eine maximale Länge (konfigurierbar, z.B. 300 Zeichen) gekürzt werden, wobei versucht werden soll, an Satz- oder Wortenden zu schneiden.

## 3. Technische Anforderungen

### 3.1. Programmiersprache:
*   Python 3.x

### 3.2. Externe Bibliotheken (Beispiele basierend auf aktuellem Code):
*   `requests`: Für HTTP-Anfragen (RSS-Feeds, LLM-API).
*   `feedparser`: Zum Parsen von RSS-Feeds.
*   Standardbibliotheken: `json`, `datetime`, `time`, `html`, `re`, `os`, `logging`.

### 3.3. Konfiguration:
*   Liste der RSS-Feeds.
*   Liste der Keywords für den Vorfilter.
*   Liste der IT-Kategorien für den LLM-Relevanz-Prompt.
*   LLM-Modellname.
*   Rate-Limit für LLM-API-Aufrufe.
*   Maximale Länge für Artikelzusammenfassungen.

### 3.4. Fehlerbehandlung und Logging:
*   Umfassendes Logging (DEBUG, INFO, WARNING, ERROR) für alle wichtigen Schritte, insbesondere für API-Aufrufe (Requests und Responses), Fehler und Verarbeitungsentscheidungen.
*   Robuste Fehlerbehandlung für Netzwerkprobleme, API-Fehler, Parsing-Fehler etc.
*   Das Logging-Format soll Zeitstempel, Loglevel, Funktionsname und die Nachricht enthalten.

## 4. Nicht-funktionale Anforderungen

### 4.1. Performance:
*   Das Abrufen und Verarbeiten der Feeds sollte in einer angemessenen Zeit erfolgen. Die LLM-Aufrufe sind der wahrscheinlichste Flaschenhals und werden durch das Rate Limiting beeinflusst.

### 4.2. Wartbarkeit:
*   Der Code sollte gut strukturiert, modular und kommentiert sein, um zukünftige Anpassungen und Erweiterungen zu erleichtern.

### 4.3. Benutzbarkeit:
*   Die generierte HTML-Datei soll übersichtlich und einfach zu navigieren sein. Die Konsolenausgaben des Skripts sollen informativ sein.

## 5. Optionale Erweiterungen (Out of Scope für die initiale Neuentwicklung, aber denkbar)

*   Persistente Speicherung der gesammelten Artikel (z.B. in einer Datenbank), um historische Analysen zu ermöglichen oder das erneute Verarbeiten bereits bekannter Artikel zu vermeiden.
*   Konfigurierbarkeit über eine externe Konfigurationsdatei statt Hartcodierung im Skript.
*   Erweiterte Deduplizierungsalgorithmen (z.B. Ähnlichkeitsberechnung).
*   Benutzeroberfläche (Web-Interface) zur Anzeige der Nachrichten und Konfiguration der Quellen.
*   Serverseitige Aktualisierung der Statistiken in der HTML-Datei ohne JavaScript.