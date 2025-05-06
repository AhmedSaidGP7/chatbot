from flask import Flask, request
import requests
import openai

app = Flask(__name__)

# 🔑 Your API keys here
VERIFY_TOKEN = "mywhatsappbot"
WHATSAPP_TOKEN = "EAAJ2ZA2ZBiOWcBO4jQsO6Y9DiZBkGoN27hUtvxEu7qFVRFSMKvxOt4soTytuDp5XzetIQGTPxqoxs0VdUytwUq5uGh1QXpp2t1G1KPVcIEmqS7xI6WgbADeXRi4RYplkJk9l82nfUlzpzzEMZAr1IXyDaKQjbL4JYfDkilSojWdKRSxPQNHqTc69tm2R1XPZAzs9d9ieHmmnurdwuiQW03DKVPDYZD"
OPENAI_API_KEY = "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"

openai.api_key = OPENAI_API_KEY

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        # Verify token with Meta
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Invalid verification token", 403

    if request.method == "POST":
        data = request.get_json()
        try:
            message = data["entry"][0]["changes"][0]["value"]["messages"][0]
            sender = message["from"]
            text = message["text"]["body"]

            # 💬 Send message to OpenAI
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "أنت مساعد ذكي يرد على العملاء باللغة العربية بطريقة ودية ومهنية."},
                    {"role": "user", "content": text}
                ]
            )
            reply = response.choices[0].message["content"]

            # 📤 Send reply to WhatsApp
            url = "https://graph.facebook.com/v18.0/591484650721893/messages"
            headers = {
                "Authorization": f"Bearer {WHATSAPP_TOKEN}",
                "Content-Type": "application/json"
            }
            payload = {
                "messaging_product": "whatsapp",
                "to": sender,
                "type": "text",
                "text": {"body": reply}
            }
            requests.post(url, headers=headers, json=payload)

        except Exception as e:
            print("Error:", e)

        return "OK", 200

if __name__ == "__main__":
    app.run(debug=True)
