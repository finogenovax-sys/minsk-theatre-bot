
import os
import json
import urllib.parse
import urllib.request

token = os.environ["TELEGRAM_BOT_TOKEN"]
chat_id = os.environ["TELEGRAM_CHAT_ID"]

message = (
    "🎭 Театр кукол Минск\n"
    "✅ Тестовое сообщение!\n\n"
    "Бот подключён к Telegram.\n"
    "Это проверка уведомлений, не настоящая бронь."
)

data = urllib.parse.urlencode({
    "chat_id": chat_id,
    "text": message
}).encode("utf-8")

request = urllib.request.Request(
    f"https://api.telegram.org/bot{token}/sendMessage",
    data=data,
    method="POST"
)

with urllib.request.urlopen(request, timeout=20) as response:
    result = json.load(response)

if not result.get("ok"):
    raise RuntimeError("Telegram не подтвердил отправку")

print("Тестовое сообщение отправлено")
