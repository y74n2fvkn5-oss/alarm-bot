import time
import requests

# Настройки конфигурации
ALERTS_API_TOKEN = "13b3f6caec12374216591727c14e354dd2b6af37ab2203"
TELEGRAM_BOT_TOKEN = "⁠8933448303:AAGocnOGnKkFW6p3sz8GVpkgeEq0eDNy0ec⁠"
CHANNEL_ID = "@ppivdenyy1"

# Отслеживаемые регионы
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
    url = "https://api.alerts.in.ua/v1/iot/active_air_raid_alerts_by_district.json"
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
                        "Ізмаїльський район", "Подільський район",
                        "Роздільнянський район"
                    ]:
                        active_info[odesa_district] = alert.get("active_alert", False)
                elif loc_title in TARGET_LOCATIONS:
                    active_info[loc_title] = alert.get("active_alert", False)
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
        response = requests.post(url, json=payload, timeout=10)
        print(f"Telegram response: {response.text}")
    except Exception as e:
        print(f"Telegram error: {e}")

print("Script started monitoring locations:", TARGET_LOCATIONS)

# Тестовое сообщение при запуске для проверки связи
send_telegram_message("✏️ Тест: бот успешно запущен и проверяет связь с каналом!")

while True:
    active_alarms = check_alarms()
    if active_alarms is not None:
        for loc in TARGET_LOCATIONS:
            is_active = loc in active_alarms and active_alarms[loc]
            if current_statuses[loc] is None:
                current_statuses[loc] = is_active
                print(f"Initial status for {loc}: {'ALERT' if is_active else 'NO ALERT'}")
            elif is_active != current_statuses[loc]:
                current_statuses[loc] = is_active
                status_text = "🚨 **УВАГА! Повітряна тривога!**" if is_active else "✅ **Відбій повітряної тривоги.**"
                message = f"{status_text}\n📍 <b>{loc}</b>"
                send_telegram_message(message)
    
    time.sleep(15)
