from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__, template_folder="templates", static_folder="static")

# FAQ responses
responses = {
    "hello": "Hello! How can I help you?",
    "hi": "Hi there!",
    "what can you do": "I can answer your questions about our courses, fees, and contact information.",
    "what courses do you offer": "We offer web development and Python courses.",
    "what is your name": "I am an AI Chatbot.", 
    "how are you": "I am doing well.",
    "what is your name": "I am an AI Chatbot.",
    "bye": "Goodbye! Have a nice day.",
    "course": "We offer web development and Python courses.",
    "fees": "Please contact administration for fee details.",
    "contact": "You can contact us at support@example.com."
}

def create_db():
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chats(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_message TEXT,
        bot_response TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()

create_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():

    user_message = request.json["message"].lower()

    bot_response = "Sorry, I don't understand that."

    for key in responses:
        if key in user_message:
            bot_response = responses[key]
            break

    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO chats(user_message, bot_response, timestamp) VALUES (?, ?, ?)",
        (
            user_message,
            bot_response,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    )

    conn.commit()
    conn.close()

    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(debug=True)