#!/usr/bin/env python3
"""
Simple HTTP health check server for Azure Container Apps.
Runs on port 8000 and responds to /health endpoint.
"""
import http.server
import socketserver
import json
import time
import threading
import os
import sys

class HealthHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health' or self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "status": "healthy",
                "service": "hermes-bot",
                "timestamp": time.time(),
                "version": "1.0"
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        # Suppress default log messages
        pass

def run_health_server(port=8000):
    with socketserver.TCPServer(("", port), HealthHandler) as httpd:
        print(f"Health check server running on port {port}", flush=True)
        httpd.serve_forever()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    run_health_server(port)