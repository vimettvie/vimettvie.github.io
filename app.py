import yt_dlp
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/get_video', methods=['GET'])
def get_video():
    video_url = request.args.get('url')
    
    if not video_url:
        return jsonify({"error": "Where link? 🤨"}), 400

    ydl_opts = {
        'format': 'best', 
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            video_direct_url = info.get('url')
            title = info.get('title')

            return jsonify({
                "status": "success",
                "title": title,
                "download_link": video_direct_url,
                "msg": "Done! 🎬🦾"
            })
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
