from flask import Flask, render_template, request
from dotenv import load_dotenv
import requests
import os

load_dotenv()

app = Flask(__name__)

OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")


@app.route("/", methods=["GET", "POST"])
def home():
    note = ""
    result = ""

    if request.method == "POST":
        note = request.form.get("note", "")

        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": MODEL,
                "prompt": f"Summarize this note in simple bullet points:\n\n{note}",
                "stream": False
            }
        )

        if response.ok:
            result = response.json()["response"]
        else:
            result = f"Error: {response.text}"

    return render_template("index.html", note=note, result=result)


if __name__ == "__main__":
    app.run(debug=True)