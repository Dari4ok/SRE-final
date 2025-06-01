import os
from flask import Flask, request

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

@app.route("/", methods=["POST"])
def alert_webhook():
    data = request.json 
    alerts = data.get("alerts", [])
    for alert in alerts:
        summary = alert.get("annotations", {}).get("summary", "")
        description = alert.get("annotations", {}).get("description", "")
        message = f"🚨 *{summary}*\n{description}"
        import requests
        requests.post(
            TELEGRAM_API_URL,
            json={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": message,
                "parse_mode": "Markdown"
            }
        )
    return "", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
