import traceback
from http.server import SimpleHTTPRequestHandler

import settings
from errors import MethodNotAllowed
from errors import NotFound
from utils import normalize_path
from utils import read_static
from utils import to_bytes


def get_path_with_file(url) -> tuple:
    path = normalize_path(url)
    parts = path.split("/")

    try:
        file_path = parts[2]
    except IndexError:
        file_path = None
    path = normalize_path(parts[1])
    path = f"/{path}" if path != "/" else path

    return path, file_path


def get_content_type_from_file(file_path: str) -> str:
    if not file_path:
        return "text/html"
    try:
        ext = file_path.split(".")[1].lower()
        content_type_by_extension = {
            "gif": "image/gif",
            "jpeg": "image/jpeg",
            "jpg": "image/jpg",
            "png": "image/png",
            "svg": "image/svg+xml",
            "ico": "image/x-icon",
        }

        content_type = content_type_by_extension[ext]
        return content_type
    except IndexError:
        pass


class MyHttp(SimpleHTTPRequestHandler):
    def do_GET(self):
        path, \
        file_path = get_path_with_file(self.path)
        content_type = get_content_type_from_file(file_path)
        endpoints = {
            "/": [self.handle_static, ["index.html", "text/html"]],
            "/style/": [self.handle_static, ["styles/Style.css", "code=404", "text/css"]],
            "/style404/": [self.handle_static, ["styles/Style404.css", "code=404", "text/css"]],
            "/bg/": [self.handle_static, ["images/back.jpg", "image/jpg"]],
            # "/pchel/": [self.handle_static, ["images/pchel.png", "image/png"]],

            "/img/": [self.handle_static, [f"images/{file_path}", content_type]],
            # "/imgg/": [self.handle_static, ["images/imgg.jpg", "image/jpg"]],
            "/hello/": [self.handle_hello, []],
            "/0/": [self.handle_zde, []],
        }

        try:
            handler, args = endpoints[path]
            handler(*args)
        except (NotFound, KeyError):
            self.handle_static("404.html", "text/html")
        except MethodNotAllowed:
            self.handle_405()
        except Exception:
            self.handle_500()

    def handle_hello(self):
        content = f"""
        <html>
        <head><title>Hello Page</title></head>
        <body>
        <h1>Hello world!</h1>
        <p>path: {self.path}</p>
        </body>
        </html>
        """

        self.respond(content)

    def handle_zde(self):
        x = 1 / 0

    def handle_static(self, file_path, ct):
        content = read_static(file_path)
        self.respond(content, code=200, content_type=ct)

    def handle_405(self):
        self.respond("", code=405, content_type="text/plain")

    def handle_500(self):
        self.respond(traceback.format_exc(), code=500, content_type="text/plain")

    def respond(self, message, code=200, content_type="text/html"):
        payload = to_bytes(message)

        self.send_response(code)
        self.send_header("Content-type", content_type)
        self.send_header("Content-length", str(len(payload)))
        self.send_header("Cache-control", f"max-age={settings.CACHE_AGE}")
        self.end_headers()
        self.wfile.write(payload)
