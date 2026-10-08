import time
import requests

ALERTS_API_TOKEN = "13b3f6caec12374216591727c14e354dd2b6af37ab2203"
TELEGRAM_BOT_TOKEN = "8933448303:AAGocnOGnKkFW6p3sz8GVpkgeEq0eDNy0ec"
CHANNEL_ID = "@ppivdenyy1"

TARGET_LOCATIONS = [
    "Одеський район",
    "Березівський район",
    "Білгород-Дністровський район",
    "Болградський район",
    "Ізмаїльський район",
    "Подільський район",
    "Роздільнянський район",
    "Криворізький район",
    "Кам'янський район",
    "Нікопольський район"
]

current_statuses = {loc: None for loc in TARGET_LOCATIONS}

def check_alarms():
    url = "https://api.alerts.in.ua/v1/alerts/active.json"
    headers = {"Authorization": f"Bearer {ALERTS_API_TOKEN}"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            alerts = data.get("alerts", [])
            active_info = {}
            for alert in alerts:
                loc_title = alert.get("location_title")
                if loc_title == "Одеська область":
                    for odesa_district in [
                        "Одеський район", "Березівський район", 
                        "Білгород-Дністровський район", "Болградський район", 
                        "Ізмаїльський район", "Подільський район", "Роздільнянський район"
                    ]:
                        active_info[odesa_district] = alert.get("alert_type", "повітряна тривога")
                elif loc_title in TARGET_LOCATIONS:
                    active_info[loc_title] = alert.get("alert_type", "повітряна тривога")
            return active_info
        else:
            print(f"API Error: {response.status_code}")
    except Exception as e:
        print(f"Connection error: {e}")
    return None

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHANNEL_ID, "text": text, "parse_mode": "HTML"}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Telegram error: {e}")

print("Script started monitoring locations:", TARGET_LOCATIONS)

while True:
    send_telegram_message("🧪 Тест: бот успешно отправляет сообщения в канал!")

    active_alarms = check_alarms()
    if active_alarms is not None:
        for loc in TARGET_LOCATIONS:
            is_active = loc in active_alarms
            if current_statuses[loc] is None:
                current_statuses[loc] = is_active
                print(f"Initial status for {loc}: {'ALERT' if is_active else 'NO ALERT'}")
            elif is_active != current_statuses[loc]:
                current_statuses[loc] = is_active
                if is_active:
                    alert_type = active_alarms.get(loc, "повітряна тривога").lower()
                    message = f"🔴 <b>{loc}</b> — повітряна тривога, червоний рівень: {alert_type.capitalize()} (червоний рівень)"
                else:
                    message = f"🟢 <b>{loc}</b> — ВІДБІЙ повітряної тривоги!"
                send_telegram_message(message)
                print(f"Sent message for {loc}: {message}")
    time.sleep(15)

