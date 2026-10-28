from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

COBALT_API = "https://api.cobalt.tools/"

@app.route('/api/info')
def info():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL missing"}), 400
    try:
        payload = {
            "url": url,
            "vQuality": "1080",
            "aFormat": "mp3",
            "filenamePattern": "basic"
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        r = requests.post(COBALT_API, json=payload, headers=headers, timeout=30).json()
        
        # cobalt ka naya response check
        if r.get("status") in ["error", "rate-limit"]:
            return jsonify({"error": r.get("text", "API Error")}), 500

        # frontend ko jo chahiye wahi bhej rahe hai
        return jsonify({
            "title": "Ready to Download",
            "thumbnail": "",
            "formats": [
                {"format_id": "best", "ext": "mp4", "quality": "MP4 - 1080p"},
                {"format_id": "audio", "ext": "mp3", "quality": "MP3 Audio"}
            ],
            "direct_url": r.get("url")
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/download')
def download():
    url = request.args.get('url')
    try:
        payload = {"url": url, "vQuality": "1080"}
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        r = requests.post(COBALT_API, json=payload, headers=headers).json()
        if r.get("url"):
            return redirect(r.get("url"))
        return jsonify({"error": "Direct link nahi mila"}), 500
    except Exception as e:
        return str(e), 500

@app.route('/')
def home():
    return "API Live - Cobalt v10 Mode"

if __name__ == '__main__':
    app.run()
