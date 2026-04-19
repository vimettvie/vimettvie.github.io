import requests, json
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

        # Список робочих інстансів (дзеркал)
        endpoints = [
            "https://cobalt.api.unblock.casa/api/json",
            "https://api.cobalt.tools/api/json",
            "https://cobalt-api.kwiat.xyz/api/json"
        ]

        for api in endpoints:
            try:
                r = requests.post(
                    api,
                    headers={
                        "Accept": "application/json",
                        "Content-Type": "application/json"
                    },
                    json={
                        "url": u,
                        "vQuality": "720",
                        "vCodec": "h264"
                    },
                    timeout=5
                )
                d = r.json()
                
                # Шукаємо лінк
                l = d.get('url') or (d.get('picker')[0].get('url') if d.get('picker') else None)
                
                if l:
                    s.wfile.write(json.dumps({"status": "ok", "url": l}).encode())
                    return # Виходимо, якщо знайшли
            except:
                continue # Якщо цей сервак ліг, пробуємо наступний

        # Якщо пройшли по всіх і глухо
        s.wfile.write(json.dumps({"status": "err", "msg": "ALL_NODES_BLOCKED"}).encode())
