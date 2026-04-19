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
                with open(cookie_path, "w") as f:
                    f.write("# Netscape HTTP Cookie File\n")
                    for c in json.loads(raw_cookies):
                        domain = c.get('domain', '')
                        flag = "TRUE" if domain.startswith(".") else "FALSE"
                        f.write(f"{domain}\t{flag}\t{c.get('path', '/')}\t{'TRUE' if c.get('secure') else 'FALSE'}\t{int(c.get('expirationDate', 0))}\t{c.get('name', '')}\t{c.get('value', '')}\n")
            opts = {
                'cookiefile': cookie_path if raw_cookies else None,
                'quiet': True,
                'no_warnings': True,
                'nocheckcertificate': True,
            }

            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(u, download=False)
                formats = info.get('formats', [])
                good_formats = [f for f in formats if f.get('acodec') != 'none' and f.get('vcodec') != 'none' and f.get('url')]
                good_formats.sort(key=lambda x: x.get('height', 0), reverse=True)

                if good_formats:
                    best = good_formats[0]
                    res = {
                        "status": "ok",
                        "url": best['url'],
                        "title": info.get('title'),
                        "quality": best.get('height')
                    }
                else:
                    res = {"status": "err", "msg": "YouTube restricted direct formats for this video"}
                
                s.wfile.write(json.dumps(res).encode())

        except Exception as e:
            s.wfile.write(json.dumps({"status": "err", "msg": str(e)}).encode())
        finally:
            if os.path.exists(cookie_path): os.remove(cookie_path)
