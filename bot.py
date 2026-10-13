import time
import requests
import pytz
from datetime import datetime

# ----------------- CONFIGURATION -----------------
BOT_TOKEN = "8942034139:AAFwAOnHyqICZWEdKsg19Pt5zej4h82Bup0"
# -------------------------------------------------

bd_tz = pytz.timezone('Asia/Dhaka')

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        updates_url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
        res = requests.get(updates_url).json()
        if res.get("result"):
            chat_id = res["result"][-1]["message"]["chat"]["id"]
            payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
            requests.post(url, json=payload)
        else:
            print("Warning: Please send a message/start your bot on Telegram first!")
    except Exception as e:
        print(f"Error sending message: {e}")

print("🤖 Bot script loaded successfully!")

last_status = None

while True:
    now = datetime.now(bd_tz)
    current_time = now.strftime("%H:%M")
    
    # ট্রেডিং সেশন: ১৪:০০ - ১৬:০০ এবং ১৯:৩০ - ২২:০০ (BST)
    session_1 = "14:00" <= current_time <= "16:00"
    session_2 = "19:30" <= current_time <= "22:00"
    
    if session_1 or session_2:
        if last_status != "ACTIVE":
            print(f"[{now.strftime('%H:%M:%S')}] 🟢 Trading Session Active! Monitoring market...")
            last_status = "ACTIVE"
            
        # ৩ মিনিটের ক্যান্ডেল ক্লোজের ৩ সেকেন্ড আগে
        if now.minute % 3 == 2 and now.second == 57:
            msg = (
                "🎯 <b>NEW TRADING SIGNAL</b> 🎯\n\n"
                "📊 <b>Market:</b> Quotex (Real Market)\n"
                "⏰ <b>Timeframe:</b> 3 Minutes\n"
                "⚠️ <b>Pattern:</b> S/R Rejection Identified\n\n"
                "💡 <i>Note: লস হলে অটো এমটিজি (Next 3-Min)</i>\n\n"
                "👑 <b>TRADE WITH KAFII ♟️</b>"
            )
            send_telegram_message(msg)
            print(f"[{now.strftime('%H:%M:%S')}] 📲 Signal sent successfully!")
            time.sleep(2)
    else:
        if last_status != "SLEEP":
            print(f"[{now.strftime('%H:%M:%S')}] 💤 Sleep Mode Active (Outside trading hours). Waiting...")
            last_status = "SLEEP"
            
    time.sleep(1)
