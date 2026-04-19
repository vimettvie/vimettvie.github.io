import requests, json, re
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

        try:
            # Спроба через інший шлюз (AIO)
            # Ми шлемо запит на сервіс, який агрегує різні методи скачування
            r = requests.post(
                "https://api.download.tube/info",
                params={"url": u},
                timeout=10
            )
            d = r.json()
            
            # Шукаємо лінк у купі даних, які вони повертають
            streams = d.get('streams', [])
            # Шукаємо mp4 з відео та аудіо (найкраща якість)
            video = next((s for s in streams if s.get('extension') == 'mp4' and s.get('url')), None)
            
            if video:
                s.wfile.write(json.dumps({
                    "status": "ok", 
                    "url": video['url'], 
                    "title": d.get('title', 'Video')
                }).encode())
                return
            
            # Якщо перший не спрацював, пробуємо запасний через інший API
            r2 = requests.get(f"https://api.boxvideo.top/api/video?url={u}", timeout=5)
            d2 = r2.json()
            if d2.get('url'):
                s.wfile.write(json.dumps({"status": "ok", "url": d2['url']}).encode())
                return

        except Exception as e:
            s.wfile.write(json.dumps({"status": "err", "msg": "STILL_BLOCKED"}).encode())

        s.wfile.write(json.dumps({"status": "err", "msg": "LAST_CHANCE_FAILED"}).encode())
