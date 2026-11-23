#!/usr/bin/env bash
# Telegram-Notifier des News Collectors — dünner Wrapper um den maschinenweiten Helper.
# Credentials, Status-Kanal und Fallback löst ~/.claude/bin/notify-telegram selbst.
#   scripts/notify_telegram.sh "✅ <b>News Collector</b>: 23 Artikel"
#   echo "mehrzeilige Nachricht" | scripts/notify_telegram.sh
# Exit 0 = gesendet · 1 = Fehler · 2 = leere Nachricht. Aufrufer hängen `|| true` an.
exec "${HOME}/.claude/bin/notify-telegram" --status "$@"
