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

        # Витягуємо ID відео
        v_id = ""
        if "v=" in v_url: v_id = v_url.split("v=")[1].split("&")[0]
        elif "youtu.be/" in v_url: v_id = v_url.split("youtu.be/")[1].split("?")[0]

        if not v_id:
            s.wfile.write(json.dumps({"status": "err", "msg": "bad_id"}).encode())
            return

        # Список публічних інстансів Invidious
        nodes = [
            f"https://invidious.lunar.icu/api/v1/videos/{v_id}",
            f"https://inv.tux.pizza/api/v1/videos/{v_id}",
            f"https://invidious.projectsegfau.lt/api/v1/videos/{v_id}"
        ]

        for node in nodes:
            try:
                r = requests.get(node, timeout=5)
                d = r.json()
                
                # Шукаємо формат mp4 (зазвичай це комбінований формат)
                formats = d.get('formatStreams', [])
                if formats:
                    # Беремо перший лінк (зазвичай 360p або 720p з аудіо)
                    f_url = formats[0].get('url')
                    if f_url:
                        s.wfile.write(json.dumps({
                            "status": "ok", 
                            "url": f_url, 
                            "title": d.get('title', 'Video')
                        }).encode())
                        return
            except:
                continue

        s.wfile.write(json.dumps({"status": "err", "msg": "NO_NODES_WORKING"}).encode())
