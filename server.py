import os
import http.server
import socketserver
import json
import subprocess
import re

PORT = int(os.environ.get("PORT", 8080))

class JavaBridgeHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path.startswith('/index.html'):
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            with open('index.html', 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_error(404, "File Not Found")

    def do_POST(self):
        if self.path == '/process':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            user_text = data.get('text', '')

            
            process = subprocess.Popen(
                ['java', 'FrequencyFingerprint'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Feed text directly into System.in
            stdout, _ = process.communicate(input=user_text + '\n')

            # Parse lines output by System.out ("A= \t0", "B= \t1", etc.)
            frequencies = {}
            for line in stdout.splitlines():
                match = re.match(r'^([A-Z])=\s+(\d+)', line)
                if match:
                    frequencies[match.group(1)] = int(match.group(2))

            # Send JSON frequency counts back to frontend
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(frequencies).encode('utf-8'))

with socketserver.TCPServer(("", PORT), JavaBridgeHandler) as httpd:
    print(f"Server running on port {PORT}")
    httpd.serve_forever()
