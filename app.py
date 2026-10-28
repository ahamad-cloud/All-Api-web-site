from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app) # Isse white screen wala error khatam

@app.route('/api/info')
def info():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL nahi diya"}), 400

    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'extractor_args': {
            'youtube': {'player_client': ['android']},
            'instagram': {'app_id': '936619743392459'}
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            data = ydl.extract_info(url, download=False)
            formats = []
            for f in data.get('formats', [])[-10:]: # last 10 hi dikhayenge
                if f.get('vcodec') != 'none' or f.get('acodec') != 'none':
                    formats.append({
                        "format_id": f['format_id'],
                        "ext": f['ext'],
                        "quality": f.get('format_note') or f.get('height', '') or 'mp4'
                    })
            
            return jsonify({
                "title": data.get('title'),
                "thumbnail": data.get('thumbnail'),
                "formats": formats[::-1] # best pehle
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/download')
def download():
    url = request.args.get('url')
    fid = request.args.get('format_id')
    ydl_opts = {
        'quiet': True,
        'format': fid,
        'user_agent': 'Mozilla/5.0'
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return redirect(info['url'])
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run()
