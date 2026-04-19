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

        # Пробуємо цей інстанс, він зараз найживіший
        api_url = "cobalt.hot-as.it" 
        # Якщо знову буде NameResolutionError, спробуй цей: "https://api.cobalt.tools/"
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        payload = {
            "url": v_url,
            "videoQuality": "720"
        }

        try:
            # Збільшуємо таймаут, бо Cobalt іноді довго думає
            r = requests.post(api_url, json=payload, headers=headers, timeout=15)
            
            # Якщо перший сервак лежить, ми миттєво переключаємося на резервний
            if r.status_code != 200:
                fallback_url = "https://api.cobalt.tools/"
                r = requests.post(fallback_url, json=payload, headers=headers, timeout=15)

            data = r.json()
            
            # В v10 посилання лежить прямо в data['url']
            if data.get('url'):
                res = {
                    "status": "ok",
                    "url": data.get('url'),
                    "title": "Success (Final Boss Defeated)"
                }
            else:
                res = {"status": "err", "msg": data.get('text', 'API returned no URL')}
            
            s.wfile.write(json.dumps(res).encode())

        except Exception as e:
            s.wfile.write(json.dumps({"status": "err", "msg": f"Final Attempt Error: {str(e)}"}).encode())
