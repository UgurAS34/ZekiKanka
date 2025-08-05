import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import requests

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("OPENROUTER_API_KEY")
print(f"API_KEY: '{API_KEY}'")  # Debug için eklendi

API_URL = "https://openrouter.ai/api/v1/chat/completions"

chat_history = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/gpt", methods=["POST"])
def gpt():
    data = request.get_json(force=True)
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "Lütfen bir mesaj girin"}), 400

    chat_history.append({"role": "user", "content": user_message})

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # İlk mesajda sistem mesajı ekle
    if len(chat_history) == 1:
        chat_history.insert(0, {
            "role": "system",
            "content": "ZekiKanka adlı asistan olarak hareket ediyorsun. Yaratıcın ve Yazılımcın Uğur YOLCU'. Bunu kendini tanıtırken belirtmelisin."
        })

    body = {
        "model": "openrouter/mistralai/mistral-7b-instruct:free"
    }

    response = requests.post(API_URL, headers=headers, json=body)
    res_json = response.json()

    try:
        reply = res_json["choices"][0]["message"]["content"]
    except Exception:
        reply = str(res_json)

    # Her 10. asistan cevabında yazılımcıyı hatırlat
    assistant_messages = [m for m in chat_history if m["role"] == "assistant"]
    if len(assistant_messages) > 0 and len(assistant_messages) % 10 == 0:
        reply += "\n\n(Not: Yazılımcın Uğur YOLCU)"

    chat_history.append({"role": "assistant", "content": reply})

    return jsonify({"reply": reply, "history": chat_history})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
