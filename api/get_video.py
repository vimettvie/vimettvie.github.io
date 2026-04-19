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
                'ignoreerrors': True,
                'format': '18/22/best', 
                'no_check_certificate': True,
                'youtube_include_dash_manifest': False, 
                'youtube_include_hls_manifest': False,
            }

            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(u, download=False)
                
                if not info:
                    raise Exception("YouTube denied info. IP might be flagged.")
                url = info.get('url')
                if not url and 'formats' in info:
                    for f in info['formats']:
                        if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                            url = f.get('url')
                            break

                if url:
                    s.wfile.write(json.dumps({"status": "ok", "url": url, "title": info.get('title')}).encode())
                else:
                    s.wfile.write(json.dumps({"status": "err", "msg": "Could not find progressive format"}).encode())

        except Exception as e:
            s.wfile.write(json.dumps({"status": "err", "msg": str(e)}).encode())
        finally:
            if os.path.exists(cookie_path): os.remove(cookie_path)
