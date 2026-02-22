from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Get Groq API key from environment variable
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    try:
        user_question = request.json.get("question")

        if not user_question:
            return jsonify({"answer": "Please enter a question."})

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama3-70b-8192",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful AI tutor for students from class 6 to competitive exams. Give structured, detailed answers."
                    },
                    {
                        "role": "user",
                        "content": user_question
                    }
                ],
                "temperature": 0.7
            }
        )

        data = response.json()
        ai_reply = data["choices"][0]["message"]["content"]

        return jsonify({"answer": ai_reply})

    except Exception as e:
        return jsonify({"answer": "Error occurred. Please check API key or try again."})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
