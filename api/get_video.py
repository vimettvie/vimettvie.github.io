import requests, json
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
        
        if not v_url: return
        api_url = "https://api.cobalt.tools/api/json"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        payload = {
            "url": v_url,
            "vQuality": "720",
            "filenameStyle": "basic"
        }

        try:
            r = requests.post(api_url, json=payload, headers=headers, timeout=10)
            data = r.json()
            
            if data.get('status') == 'stream' or data.get('status') == 'picker':
                res = {
                    "status": "ok",
                    "url": data.get('url'),
                    "title": "YouTube Video"
                }
            else:
                res = {"status": "err", "msg": data.get('text', 'Cobalt error')}
            
            s.wfile.write(json.dumps(res).encode())

        except Exception as e:

            s.wfile.write(json.dumps({"status": "err", "msg": f"External API Error: {str(e)}"}).encode())
