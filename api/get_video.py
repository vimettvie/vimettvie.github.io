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
            api = "https://api.cobalt.tools/api/json"
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            payload = {
                "url": v_url,
                "videoQuality": "720",
                "vCodec": "h264",
                "isAudioOnly": False
            }
            
            r = requests.post(api, json=payload, headers=headers)
            data = r.json()

            if data.get('status') == 'stream':
                res = {
                    "status": "ok",
                    "url": data.get('url'),
                    "title": "Video Ready"
                }
            elif data.get('status') == 'redirect':
                res = {
                    "status": "ok",
                    "url": data.get('url'),
                    "title": "Redirect Ready"
                }
            else:
                res = {"status": "error", "msg": data.get('text')}

            s.wfile.write(json.dumps(res).encode())

        except Exception as e:
            s.wfile.write(json.dumps({"status": "error", "dev": str(e)}).encode())
