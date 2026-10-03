import http.server
import socketserver
import json
import subprocess
import re

PORT = 8000

class JavaBridgeHandler(http.server.SimpleHTTPRequestHandler):
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

            
            stdout, _ = process.communicate(input=user_text + '\n')

            
            frequencies = {}
            for line in stdout.splitlines():
                match = re.match(r'^([A-Z])=\s+(\d+)', line)
                if match:
                    frequencies[match.group(1)] = int(match.group(2))

            # Send JSON back to HTML
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(frequencies).encode('utf-8'))

with socketserver.TCPServer(("", PORT), JavaBridgeHandler) as httpd:
    print(f"Server running at http://localhost:{PORT}")
    httpd.serve_forever()
