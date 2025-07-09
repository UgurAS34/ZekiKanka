import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import requests

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/gpt", methods=["POST"])
def gpt():
    data = request.get_json(force=True)
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "Lütfen bir mesaj girin"}), 400

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "openrouter/cypher-alpha:free",
        "messages": [
            {"role": "system", "content": "Sen ZekiKanka adlı asistan olarak hareket ediyorsun. Yaratıcın ve yazılımcın Uğur YOLCU'dur. Bu sorulduğunda bunu kesinlikle belirtmelisin."},
            {"role": "user", "content": user_message}
        ],
        "stream": False
    }

    response = requests.post(API_URL, headers=headers, json=body)
    res_json = response.json()

    try:
        reply = res_json["choices"][0]["message"]["content"]
    except Exception:
        reply = str(res_json)

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
