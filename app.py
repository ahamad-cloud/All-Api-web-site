from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp, os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"status": "API Live Hai"})

@app.route('/api/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url') if data else None
    if not url:
        return jsonify({"error": "Link bhejo"}), 400
    opts = {'format': 'best[ext=mp4]/best', 'quiet': True, 'noplaylist': True}
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({"title": info.get('title'), "thumbnail": info.get('thumbnail'), "download_url": info.get('url')})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
