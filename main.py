from flask import Flask, render_template, request, jsonify
import json
from openai import OpenAI

app = Flask(__name__)

try:
    with open("secret.json") as f:
        secrets = json.load(f)
        api_key = secrets["api_key"]
    client = OpenAI(api_key=api_key)
except FileNotFoundError:
    print("The file 'secrets.json' was not found.")
except KeyError:
    print("The 'api_key' was not found in 'secrets.json'.")

def get_chat_response(messages):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=1.0
    )
    return response.choices[0].message

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process_input", methods=["POST"])
def process_input():
    user_input = request.form["user_input"]
    messages = [
        {"role": "system", "content": f"Sei un assistente virtuale chiamato Pyum Ai e parli italiano."},
        {"role": "user", "content": user_input}
    ]
    new_message = get_chat_response(messages)
    return jsonify({"assistant_response": new_message.content})

if __name__ == "__main__":
    app.run(debug=True)
    app.run(debug=True, use_reloader=True)
