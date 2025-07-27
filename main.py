from flask import Flask, request, jsonify
import openai
import os
import traceback

app = Flask(__name__)
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def home():
    return "✅ Stoic AI Webhook is running."

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        user_input = data.get("message", "")

        prompt = f"""Tu es un guide stoïcien bienveillant. L'utilisateur écrit :
\"{user_input}\"

Réponds-lui avec une réflexion inspirée de Marc Aurèle, Sénèque ou Épictète :
→"""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0.7
        )
        result = response.choices[0].message['content'].strip()
        return jsonify({"response": result})

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("🧘 Lancement de Stoic AI Webhook...")
    app.run(host="0.0.0.0", port=8080)
