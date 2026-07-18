from flask import Flask, send_file
from renderer import render_dashboard

app = Flask(__name__)


@app.route("/")
def home():
    render_dashboard()
    return send_file("output/dashboard.png", mimetype="image/png")


@app.route("/dashboard.png")
def dashboard():
    render_dashboard()
    return send_file("output/dashboard.png", mimetype="image/png")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8090, debug=True)
