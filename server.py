import traceback
from datetime import datetime
from http.server import SimpleHTTPRequestHandler

import settings
from custom_types import HttpRequest
from errors import MethodNotAllowed
from errors import NotFound
from utils import get_user_data
from utils import read_static
from utils import to_bytes


class MyHttp(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.dispatch("get")

    def do_POST(self):
        self.dispatch("post")

    def dispatch(self, http_method):
        req = HttpRequest.from_path(self.path, method=http_method)

        endpoints = {
            "/": [self.handle_static, ["index.html", "text/html"]],
            "/st/": [self.handle_static, [f"styles/{req.file_name}", req.content_type]],
            "/img/": [self.handle_static, [f"images/{req.file_name}", req.content_type]],
            "/hello/": [self.handle_hello, [req]],
            "/0/": [self.handle_zde, []],
        }

        try:
            handler, args = endpoints[req.normal]
            handler(*args)
        except (NotFound, KeyError):
            self.handle_404()
        except MethodNotAllowed:
            self.handle_405()
        except Exception:
            self.handle_500()

    def get_request_payload(self) -> str:
        content_length_in_str = self.headers.get("content-length", 0)
        content_length = int(content_length_in_str)

        if not content_length:
            return ""
        payload_in_bytes = self.rfile.read(content_length)
        payload = payload_in_bytes.decode()
        return payload

    def handle_hello(self, request):
        query_string = self.get_request_payload() or request.query_string
        user = get_user_data(query_string)
        year = datetime.now().year - int(user.age)

        content = f"""
        <html>
        <head><title>Hello Page</title></head>
        <body style="background-color:00BFFBF">
        <h1>Hello {user.name}!</h1>
        <h2>You were born in {year}</h2>
        <p>path: {self.path}</p>
            
            <form method="post">
                <div class="name"><label for="name-id">Your name:</label>
                <input type="text" name="name" id="name-id">
                </div>
                <div class="age" style="position:absolute;top:180;"><label for="year-id">Your age:</label>
                <input type="text" name="age" id="age-id">
                <button type="submit" id="greet_button-id" style="position:absolute;left:250;top:-33;height:5em">Greet</button>
                </div>           
            </form>

        </body>
        </html>
        """

        self.respond(content)

    def handle_zde(self):
        x = 1 / 0

    def handle_static(self, file_path, ct):
        content = read_static(file_path)
        self.respond(content, content_type=ct)

    def handle_404(self):
        content = read_static("404.html")
        self.respond(content, code=404, content_type="text/html")

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
