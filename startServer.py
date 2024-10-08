from http.server import HTTPServer, SimpleHTTPRequestHandler
import socket

# def get_ip_address():
#     hostname = socket.gethostname()
#     ip_address_list = socket.getaddrinfo(hostname, None)
    
#     for address in ip_address_list:
#         ip_family, _, _, _, ip_address = address
#         if ip_family == socket.AF_INET:
#             return ip_address[0]

ip = "127.0.0.1"
# get_ip_address()
port = 8080

server_address = (ip, port)
httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)

print(f"Server running at http://{ip}:{port}/")
httpd.serve_forever()