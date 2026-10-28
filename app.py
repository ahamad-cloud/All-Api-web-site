from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# 3 alag cobalt servers - ek fail hua to dusra try hoga
INSTANCES = [
    "https://api.cobalt.tools/",
    "https://co.wuk.sh/api/json",
    "https://api.galaxysd.me/api/json"
]

def get_cobalt_link(video_url):
    payload = {
        "url": video_url,
        "vQuality": "1080",
        "aFormat": "mp3",
        "filenamePattern": "basic"
    }
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    
    for api_url in INSTANCES:
        try:
            # api_url me /api/json hai to direct, nahi to root pe post
            target = api_url if "api/json" in api_url else api_url
            r = requests.post(target, json=payload, headers=headers, timeout=20)
            data = r.json()
            print(f"Trying {api_url} -> {data}") # ye Render logs me dikhega
            
            if data.get("status") == "error" or data.get("status") == "rate-limit":
                continue
            if data.get("url"):
                return data
        except Exception as e:
            print(f"Failed {api_url}: {e}")
            continue
    return None

@app.route('/api/info')
def info():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL missing"}), 400
    
    result = get_cobalt_link(url)
    if not result:
        return jsonify({"error": "All APIs failed, try again after 1 min"}), 500

    return jsonify({
        "title": "Ready to Download",
        "thumbnail": "",
        "formats": [{"format_id": "best", "ext": "mp4", "quality": "MP4 - Best"}],
        "direct_url": result.get("url")
    })

@app.route('/api/download')
def download():
    url = request.args.get('url')
    result = get_cobalt_link(url)
    if result and result.get("url"):
        return redirect(result.get("url"))
    return jsonify({"error": "Download link not found"}), 500

@app.route('/')
def home():
    return "API Live - Multi Cobalt"

if __name__ == '__main__':
    app.run()
