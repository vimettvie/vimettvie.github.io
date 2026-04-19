import yt_dlp
import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        s = self
        q = parse_qs(urlparse(s.path).query)
        u = q.get('url', [None])[0]

        s.send_response(200)
        s.send_header('Content-type', 'application/json')
        s.send_header('Access-Control-Allow-Origin', '*')
        s.end_headers()

        if not u: return

        opts = {
            'format': 'best[ext=mp4]/best',
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
            'nocheckcertificate': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'referer': 'https://www.google.com/',
        }

        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(u, download=False)
                
                link = info.get('url')
                title = info.get('title', 'Video')

                if link:
                    res = {"status": "ok", "url": link, "title": title}
                else:
                    res = {"status": "err", "msg": "No direct link"}
                
                s.wfile.write(json.dumps(res).encode())

        except Exception as e:
            err_msg = str(e)
            if "Sign in" in err_msg:
                err_msg = "YouTube blocked Vercel IP. Need cookies."
            
            s.wfile.write(json.dumps({"status": "err", "msg": err_msg}).encode())
