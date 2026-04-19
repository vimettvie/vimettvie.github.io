import yt_dlp
import json
import os
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
        cookie_path = "/tmp/cookies.txt"
        try:
            raw_cookies = os.environ.get("YT_COOKIES")
            if raw_cookies:
                cookies_json = json.loads(raw_cookies)
                with open(cookie_path, "w") as f:
                    f.write("# Netscape HTTP Cookie File\n")
                    for c in cookies_json:
                        domain = c.get('domain', '')
                        flag = "TRUE" if domain.startswith(".") else "FALSE"
                        p = c.get('path', '/')
                        sec = "TRUE" if c.get('secure') else "FALSE"
                        exp = int(c.get('expirationDate', 0))
                        name = c.get('name', '')
                        val = c.get('value', '')
                        f.write(f"{domain}\t{flag}\t{p}\t{sec}\t{exp}\t{name}\t{val}\n")
            opts = {
                'format': '22/18/best[vcodec!=none][acodec!=none]',
                'cookiefile': cookie_path if raw_cookies else None,
                'quiet': True,
                'no_warnings': True,
                'nocheckcertificate': True,
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            }
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(u, download=False)
                res = {
                    "status": "ok",
                    "url": info.get('url'),
                    "title": info.get('title')
                }
                s.wfile.write(json.dumps(res).encode())
        except Exception as e:
            s.wfile.write(json.dumps({"status": "err", "msg": str(e)}).encode())
        finally:
            if os.path.exists(cookie_path):
                os.remove(cookie_path)
