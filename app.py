from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/api/info')
def info():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL missing"}), 400
    try:
        # Cobalt API - best for YouTube, Instagram, TikTok etc
        res = requests.post("https://api.cobalt.tools/api/json", 
            json={"url": url, "vQuality": "1080", "aFormat": "mp3", "filenamePattern": "basic"},
            headers={"Accept": "application/json", "Content-Type": "application/json"}
        , timeout=30).json()

        if res.get("status") == "error":
             return jsonify({"error": res.get("text", "Cobalt error")}), 500
        
        # Frontend ke liye format bana rahe hai
        return jsonify({
            "title": res.get("text", "Video"),
            "thumbnail": "",
            "formats": [
                {"format_id": "best", "ext": "mp4", "quality": "Best Quality"},
                {"format_id": "audio", "ext": "mp3", "quality": "MP3 Audio"}
            ],
            "direct_url": res.get("url") # direct link
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/download')
def download():
    url = request.args.get('url')
    # Seedha cobalt se redirect
    try:
        r = requests.post("https://api.cobalt.tools/api/json", 
            json={"url": url}, headers={"Accept": "application/json", "Content-Type": "application/json"}).json()
        return redirect(r.get("url"))
    except Exception as e:
        return str(e), 500

@app.route('/')
def home():
    return "API is Live - Cobalt Mode"

if __name__ == '__main__':
    app.run()
