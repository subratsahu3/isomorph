"""
ISOMORPH Web Server
Lightweight embedded server providing an interactive visual dashboard for researchers.
"""

from __future__ import annotations
import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from ..core.engine import IsomorphEngine
from ..corpus.benchmark_papers import load_benchmark_corpus


class IsomorphWebHandler(BaseHTTPRequestHandler):
    engine: IsomorphEngine = None
    html_content: str = ""

    def log_message(self, format, *args):
        # Quiet standard logging to keep terminal clean
        pass

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(self.html_content.encode("utf-8"))
        elif self.path == "/api/scan":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            data = self.engine.to_json()
            self.wfile.write(data.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")


def start_server(port: int = 8000) -> None:
    engine = IsomorphEngine(similarity_threshold=0.85)
    engine.register_papers(load_benchmark_corpus())
    engine.run_scan()

    html_path = os.path.join(os.path.dirname(__file__), "dashboard.html")
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    IsomorphWebHandler.engine = engine
    IsomorphWebHandler.html_content = html_content

    server = HTTPServer(("0.0.0.0", port), IsomorphWebHandler)
    print(f"\n🚀 ISOMORPH Visual Dashboard launched at: http://localhost:{port}")
    print("Press Ctrl+C to stop the server.\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping ISOMORPH server...")
        server.server_close()
