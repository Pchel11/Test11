import traceback
from datetime import datetime
from http.server import SimpleHTTPRequestHandler

import settings
from custom_types import Endpoint
from errors import MethodNotAllowed
from errors import NotFound
from utils import get_content_type
from utils import get_user_data
from utils import read_static
from utils import to_bytes


class MyHttp(SimpleHTTPRequestHandler):
    def do_GET(self):
        endpoint = Endpoint.from_path(self.path)
        content_type = get_content_type(endpoint.file_name)

        endpoints = {
            "/": [self.handle_static, ["index.html", "text/html"]],
            "/st/": [self.handle_static, [f"styles/{endpoint.file_name}", "text/css"]],
            "/img/": [self.handle_static, [f"images/{endpoint.file_name}", content_type]],
            "/hello/": [self.handle_hello, [endpoint]],
            "/0/": [self.handle_zde, []],
        }

        try:
            handler, args = endpoints[endpoint.normal]
            handler(*args)
        except (NotFound, KeyError):
            self.handle_404()
        except MethodNotAllowed:
            self.handle_405()
        except Exception:
            self.handle_500()

    def handle_hello(self, endpoint):
        user = get_user_data(endpoint.query_string)
        year = datetime.now().year - user.age

        content = f"""
        <html>
        <head><title>Hello Page</title></head>
        <body style="background-color:00BFFBF">
        <h1>Hello {user.name}!</h1>
        <h2>You were born in {year}</h2>
        <p>path: {self.path}</p>
            
            <form>
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
