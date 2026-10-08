import time
import requests

ALERTS_API_TOKEN = "13b3f6caec12374216591727c1"
TELEGRAM_BOT_TOKEN = "8976459299:AAE0LcwUHfYR0c27i2pC5uWr0NeD646xIo"
CHANNEL_ID = "@ppivdenyy1"

TARGET_LOCATIONS = [
    "Криворізький район"
]

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHANNEL_ID, "text": text}
    try:
        response = requests.post(url, json=payload, timeout=10)
        print(f"Telegram response: {response.text}")
    except Exception as e:
        print(f"Telegram error: {e}")

# Отправляем тестовое сообщение сразу при старте
send_telegram_message("🧪 Бот запущен и настроен на Криворожский район!")

print("Скрипт запущен, работаем...")

while True:
    time.sleep(15)

    
    

