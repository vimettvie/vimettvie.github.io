import requests
import json
import os
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

        # Використовуємо один з найстабільніших API на RapidAPI
        # Тобі треба просто вставити свій ключ у змінні оточення Vercel (RAPID_API_KEY)
        api_key = os.environ.get("RAPID_API_KEY", "3dbed9723amsha66db189e9d4a2ep1c1f93jsn6a95c76d9cd6")
        
        url = "https://youtube-video-download-info.p.rapidapi.com/dl"
        querystring = {"id": v_url.split("v=")[-1].split("&")[0]} # Витягуємо ID відео

        headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "youtube-video-download-info.p.rapidapi.com"
        }

        try:
            r = requests.get(url, headers=headers, params=querystring, timeout=10)
            data = r.json()
            if data.get('status') == 'ok':
                links = data.get('link', {})
                download_url = list(links.values())[0][0] 
                res = {
                    "status": "ok",
                    "url": download_url,
                    "title": data.get('title', 'Video')
                }
            else:
                res = {"status": "err", "msg": "RapidAPI: Video not found or limit reached"}
            s.wfile.write(json.dumps(res).encode())

        except Exception as e:
            s.wfile.write(json.dumps({"status": "err", "msg": f"System Error: {str(e)}"}).encode())
