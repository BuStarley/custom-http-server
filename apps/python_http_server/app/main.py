import socketserver
from server import HttpRequestHandler, PORT
import signal
import sys

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

def signal_handler(sig, frame):
    print("\nHTTP-SERVER DOWN")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
    
with ReusableTCPServer(("", PORT), HttpRequestHandler) as httpd:
    print("HTTP-SERVER UP")
    print(f"HTTP server start with http://localhost:{PORT}")
    print("Press Ctrl+C for stop")
        
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nHTTP-SERVER DOWN")