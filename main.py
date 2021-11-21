import sys
from configparser import ConfigParser
from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape

import wine


def get_config_param(category, param):
    config = ConfigParser()
    config.read('config.ini', encoding="utf-8")
    return config.get(category, param)


def render_html():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
        )

    template = env.get_template('template.html')

    rendered_page = template.render(wines=wine.get_wines(), age=wine.get_age_factory())
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


def run_http_server():
    handler_class = SimpleHTTPRequestHandler
    server_class = HTTPServer
    protocol = "HTTP/1.0"
    if sys.argv[1:]:    # Проверка есть ли порт у адреса
        port = int(sys.argv[1])
    else:
        port = 8000
    server_address = ('127.0.0.1', port)

    handler_class.protocol_version = protocol
    httpd = server_class(server_address, handler_class)

    ip, port = httpd.socket.getsockname()
    print("Serving HTTP on", ip, "port", port, "...")
    httpd.serve_forever()


if __name__ == '__main__':
    render_html()
    run_http_server()
