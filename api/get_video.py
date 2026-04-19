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
            s.wfile.write(json.dumps({"status": "err", "msg": "No URL provided"}).encode())
            return

        # Актуальний API Cobalt (v10+)
        api_url = "https://api.cobalt.tools/"
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        # Новий формат тіла запиту для v10
        payload = {
            "url": v_url,
            "videoQuality": "720", # v10 використовує videoQuality замість vQuality
            "filenameStyle": "basic"
        }

        try:
            # Важливо: Cobalt v10 часто вимагає POST запит на корінь або /
            r = requests.post(api_url, json=payload, headers=headers, timeout=10)
            
            if r.status_code != 200:
                # Якщо головний сервер лежить, пробуємо офіційне дзеркало
                alt_url = "https://cobalt.api.v0.sh/"
                r = requests.post(alt_url, json=payload, headers=headers, timeout=10)

            data = r.json()
            
            # У v10 статус зазвичай 'tunnel', 'redirect' або 'picker'
            if data.get('status') in ['stream', 'video', 'picker', 'redirect', 'tunnel']:
                res = {
                    "status": "ok",
                    "url": data.get('url'),
                    "title": "Success (v10)"
                }
            else:
                res = {"status": "err", "msg": data.get('text', 'Cobalt API error')}
            
            s.wfile.write(json.dumps(res).encode())

        except Exception as e:
            s.wfile.write(json.dumps({"status": "err", "msg": f"API Error: {str(e)}"}).encode())
