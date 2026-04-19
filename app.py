from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/')
def home():
    return "RUNNING"

@app.route('/get_video')
def get_video():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"error": "No URL"}), 400
    
    ydl_opts = {'format': 'best', 'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        return jsonify({"url": info.get('url')})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
