from flask import Flask
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from Service 1 after cicd pipeline hello done "

@app.route("/call-service2")
def call_service2():
    resp = requests.get("http://service2:5000/")
    return f"Service1 calling -> {resp.text}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
