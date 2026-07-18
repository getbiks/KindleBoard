from flask import Flask, send_file, jsonify

app = Flask(__name__)

BASE_URL = "http://192.168.1.2:8090"


@app.route("/")
def home():
    return "KindleBoard Server"


@app.route("/dashboard.png")
def dashboard():
    return send_file("output/dashboard.png", mimetype="image/png")


@app.route("/api/display")
def api_display():

    return jsonify({
        "image_url": f"{BASE_URL}/dashboard.png",
        "filename": "dashboard.png",
        "refresh_rate": 300,
        "update_firmware": False
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8090, debug=False)
