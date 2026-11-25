#!/usr/bin/env bash
# Nächtlicher News-Collector-Lauf, per Cron gestartet.
#
# Das Skript denkt nicht — es startet den Claude-Orchestrator (scripts/nightly_prompt.md),
# der die vier Pipeline-Agenten steuert und am Ende selbst per Telegram meldet.
# Hier drin bleibt nur: Umgebung herstellen, Session-ID vergeben, Log schreiben und
# einen Notruf senden, falls Claude selbst gar nicht erst hochkommt.
#
# Cron: 0 5 * * *  /home/aroc/projects/news_collector/scripts/nightly.sh

set -uo pipefail

PROJECT="/home/aroc/projects/news_collector"
cd "$PROJECT" || exit 1

# Cron hat ein minimales PATH — claude, python und curl müssen auffindbar sein.
export PATH="/home/aroc/.local/bin:/usr/local/bin:/usr/bin:/bin"
export HOME="/home/aroc"

# Telegram-Credentials aus dem tmpfs; unter Cron ist GPG gesperrt, `pass` scheidet aus.
SECRETS="/run/user/$(id -u)/secrets.env"
if [ -f "$SECRETS" ]; then
  set -a
  # shellcheck disable=SC1090
  . "$SECRETS" 2>/dev/null || true
  set +a
fi

RUN_STAMP="$(date +%Y%m%d_%H%M%S)"
CLAUDE_SESSION_ID="$(cat /proc/sys/kernel/random/uuid)"
export RUN_STAMP CLAUDE_SESSION_ID

mkdir -p "$PROJECT/_logs" "$PROJECT/_work/news/$RUN_STAMP"
LOG="$PROJECT/_logs/nightly_$RUN_STAMP.log"

{
  echo "=== News Collector Nachtlauf $RUN_STAMP ==="
  echo "session: $CLAUDE_SESSION_ID"
} >> "$LOG"

# --dangerously-skip-permissions: unter Cron gibt es niemanden, der Prompts bestätigt.
# Der Lauf ist auf dieses Projekt beschränkt und schreibt nur nach _work/ und ins Root.
timeout 90m claude -p "$(cat "$PROJECT/scripts/nightly_prompt.md")" \
  --session-id "$CLAUDE_SESSION_ID" \
  --dangerously-skip-permissions \
  >> "$LOG" 2>&1
rc=$?

echo "=== exit $rc ===" >> "$LOG"

# Der Orchestrator meldet selbst. Nur wenn er gar nicht durchkam (Absturz, Timeout),
# gibt es hier einen Notruf — sonst bliebe der Ausfall unbemerkt.
if [ "$rc" -ne 0 ]; then
  "$PROJECT/scripts/notify_telegram.sh" \
    "❌ <b>News Collector</b> – Nachtlauf abgebrochen (exit $rc)
Der Orchestrator kam nicht durch, kein Report erzeugt.
Log: <code>$LOG</code>
🔗 Session: <code>claude --resume $CLAUDE_SESSION_ID</code>" || true
fi

exit "$rc"
