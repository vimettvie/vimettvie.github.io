import requests
import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        s = self
        q = parse_qs(urlparse(s.path).query)
        v_url = q.get('url', [None])[0]

        s.send_response(200)
        s.send_header('Content-type', 'application/json')
        s.send_header('Access-Control-Allow-Origin', '*')
        s.end_headers()

        if not v_url:
            s.wfile.write(json.dumps({"status": "error"}).encode())
            return

        try:
            r = requests.post(
                "https://api.cobalt.tools/api/json",
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                },
                json={
                    "url": v_url,
                    "videoQuality": "720",
                    "vCodec": "h264"
                },
                timeout=10
            )
            d = r.json()
            f_url = d.get('url') or (d.get('picker')[0].get('url') if d.get('picker') else None)

            if f_url:
                res = {"status": "ok", "url": f_url, "title": "Video Found"}
            else:
                res = {"status": "error", "msg": "API Blocked"}

            s.wfile.write(json.dumps(res).encode())

        except:
            s.wfile.write(json.dumps({"status": "error", "msg": "System down"}).encode())
