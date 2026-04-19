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
        
        if not v_url: return

        # Список свіжих інстансів, які зараз найменше забанені
        instances = [
            "https://api.cobalt.tools/",
            "https://cobalt.hot-as.it/",
            "https://cobalt.as93.net/",
            "https://api.v0.sh/"
        ]
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        payload = {
            "url": v_url,
            "videoQuality": "720",
            "filenameStyle": "basic"
        }

        success = False
        for api_url in instances:
            try:
                # Пробуємо кожен інстанс по черзі
                r = requests.post(api_url, json=payload, headers=headers, timeout=8)
                if r.status_code == 200:
                    data = r.json()
                    if data.get('url'):
                        s.wfile.write(json.dumps({
                            "status": "ok",
                            "url": data.get('url'),
                            "title": "Finally Found a Way!"
                        }).encode())
                        success = True
                        break
            except:
                continue # Якщо цей інстанс лежить, йдемо до наступного

        if not success:
            s.wfile.write(json.dumps({
                "status": "err", 
                "msg": "Всі дзеркала Cobalt зараз під баном YouTube. Треба почекати або оновити кукі на власному сервері."
            }).encode())
