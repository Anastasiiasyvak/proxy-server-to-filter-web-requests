#!/usr/bin/env python3

import http.server
import socketserver
import socket
import logging
import urllib.request


def get_sum_of_ip_components(peer_addr):
    try:
        ip_components = [int(x) for x in peer_addr.split('.')]
        return sum(ip_components)
    except ValueError as e:
        logging.error(f"Error while calculating sum of IP components: {e}")
        return 0


def get_fifth_column_from_proc_stat():
    try:
        with open('/proc/stat', 'r') as stat_file:
            for line in stat_file:
                if line.startswith('cpu'):
                    columns = line.split()
                    if len(columns) >= 5:
                        return int(columns[4])
    except Exception as e:
        logging.error(f"Error while reading /proc/stat: {e}")
    return 0


def calculate_result():
    A = get_sum_of_ip_components(socket.gethostbyname(socket.gethostname()))
    B = get_fifth_column_from_proc_stat()
    return (A + B) % 2


def serve_index_html():
    try:
        with urllib.request.urlopen("http://localhost:20000/index.html") as response:
            content = response.read()
        return content
    except Exception as e:
        logging.error(f"Error while serving index HTML: {e}")
        return b"Index HTML file not found"


def serve_error_html():
    try:
        with urllib.request.urlopen("http://localhost:20000/error.html") as response:
            content = response.read()
        return content
    except Exception as e:
        logging.error(f"Error while serving error HTML: {e}")
        return b"Error HTML file not found"


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(serve_index_html())
        elif self.path == '/error.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(serve_error_html())
        else:
            super().do_GET()


def main():
    logging.basicConfig(level=logging.ERROR)
    PORT = 20000
    handler = MyHttpRequestHandler


    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print("Server started at localhost:" + str(PORT))
        httpd.serve_forever()


if __name__ == "__main__":
    main()
