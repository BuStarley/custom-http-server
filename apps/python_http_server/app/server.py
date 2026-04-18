import socketserver
from dotenv import load_dotenv
import os
import urllib.parse
import mimetypes
import json
from pathlib import Path

env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(env_path)

PORT = int(os.getenv('PORT', '8080'))
STATIC_DIR = os.getenv('STATIC_DIR', './static')

class HttpRequestHandler(socketserver.StreamRequestHandler):
    def handle(self):
        try:
            request_line = self.rfile.readline().decode('utf-8').strip()
            if not request_line:
                return
            
            print(f"---> {request_line}")

            parts = request_line.split()
            if len(parts) != 3:
                self.send_error(400, "Bad request")
                return
            method, path, version = parts

            headers = {}
            while True:
                header_line = self.rfile.readline().decode('utf-8').strip()
                if not header_line:
                    break
                if ':' in header_line:
                    key, value = header_line.split(':', 1)
                    headers[key.strip().lower()] = value.strip()

            if method != 'GET':
                self.send_error(405, "Method Not Allowed")
                return
            
            if path == '/api/env-info':
                self.send_env_info()
                return
            
            parsed_url = urllib.parse.urlparse(path)
            file_path = parsed_url.path
            
            if file_path.startswith('/static/'):
                file_path = file_path[8:]
            else:
                file_path = file_path.lstrip('/')
            
            if file_path == "" or file_path == "/":
                file_path = "index.html"
            
            full_path = os.path.join(STATIC_DIR, file_path)
            
            self.serve_file(full_path)
            
        except Exception as e:
            print(f"Error: {e}")
            self.send_error(500, "Internal Server Error")
    
    def send_env_info(self):
        env_data = {
            'APP_NAME': os.getenv('APP_NAME', 'NOT SET'),
            'APP_ENV': os.getenv('APP_ENV', 'NOT SET'),
            'API_KEY': os.getenv('API_KEY', 'NOT SET'),
            'DEBUG': os.getenv('DEBUG', 'NOT SET'),
            'STATUS': 'OK'
        }
        
        body = json.dumps(env_data).encode('utf-8')
        
        self.wfile.write(b"HTTP/1.1 200 OK\r\n")
        self.wfile.write(b"Content-Type: application/json\r\n")
        self.wfile.write(f"Content-Length: {len(body)}\r\n".encode())
        self.wfile.write(b"Connection: close\r\n")
        self.wfile.write(b"\r\n")
        self.wfile.write(body)
        print(f"<-- 200 OK /api/env-info")

    def serve_file(self, full_path):
        try:
            with open(full_path, 'rb') as f:
                content = f.read()

            mime_type, _ = mimetypes.guess_type(full_path)
            if mime_type is None:
                mime_type = 'application/octet-stream'

            self.wfile.write(b"HTTP/1.1 200 OK\r\n")
            self.wfile.write(f"Content-Type: {mime_type}\r\n".encode())
            self.wfile.write(f"Content-Length: {len(content)}\r\n".encode())
            self.wfile.write(b"Connection: close\r\n")
            self.wfile.write(b"\r\n")
            self.wfile.write(content)
            print(f"<-- 200 OK {full_path}")

        except FileNotFoundError:
            self.send_error(404, "Not Found")
        except IsADirectoryError:
            new_path = os.path.join(full_path, "index.html")
            self.serve_file(new_path)
        except PermissionError:
            self.send_error(403, "Forbidden")

    def send_error(self, code, message):
        body = f"<html><body><h1>{code} {message}</h1></body></html>".encode('utf-8')
        self.wfile.write(f"HTTP/1.1 {code} {message}\r\n".encode())
        self.wfile.write(b"Content-Type: text/html; charset=utf-8\r\n")
        self.wfile.write(f"Content-Length: {len(body)}\r\n".encode())
        self.wfile.write(b"Connection: close\r\n")
        self.wfile.write(b"\r\n")
        self.wfile.write(body)
        print(f"<-- {code} {message}")