"""
Aegis - Local Development Server
Serves the frontend app for accessibility testing.
"""

import http.server
import socketserver
import os
import sys
import threading
import time

PORT = 8888
APP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app")


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP handler that suppresses request logging."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=APP_DIR, **kwargs)

    def log_message(self, format, *args):
        pass  # Suppress output


def start_server(port=PORT):
    """Start the dev server on the specified port."""
    handler = QuietHandler
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"[Aegis] Serving app at http://localhost:{port}")
        print(f"[Aegis] Serving files from: {APP_DIR}")
        print(f"[Aegis] Press Ctrl+C to stop.\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[Aegis] Server stopped.")
            httpd.shutdown()


def start_server_background(port=PORT):
    """Start the server in a background thread. Returns the thread."""
    thread = threading.Thread(target=start_server, args=(port,), daemon=True)
    thread.start()
    time.sleep(0.5)  # Give server time to start
    return thread


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
    start_server(port)
