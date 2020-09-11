import traceback

from http.server import SimpleHTTPRequestHandler

from custom_types import HttpRequest
from custom_types import User

from errors import MethodNotAllowed
from errors import NotFound

from utils import read_static
from utils import to_bytes
from utils import to_str
from utils import load_user_data
from utils import save_user_data

from pages_render import render_hello_page


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
            "/hello-update/": [self.handle_hello_update, [req]],
            "/0/": [self.handle_zde, []],
        }

        try:
            try:
                handler, args = endpoints[req.normal]
            except KeyError as err:
                raise NotFound from err

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

    def handle_hello(self, request: HttpRequest):
        if request.method != "get":
            raise MethodNotAllowed

        query = load_user_data()
        user = User.build(query)

        content = render_hello_page(user, user)

        self.respond(content)

    def handle_hello_update(self, request: HttpRequest):
        if request.method != "post":
            raise MethodNotAllowed

        form_data = self.get_form_data()
        new_user = User.build(form_data)

        if not new_user.errors:
            save_user_data(form_data)
            self.redirect("/hello")
            return

        saved_data = load_user_data()
        saved_user = User.build(saved_data)

        hello_page = render_hello_page(new_user, saved_user)

        self.respond(hello_page)

    @staticmethod
    def handle_zde():
        x = 1 / 0
        print(x)

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
        self.end_headers()
        self.wfile.write(payload)

    def redirect(self, to):
        self.send_response(302)
        self.send_header("Location", to)
        self.end_headers()

    def get_form_data(self) -> str:
        content_length_as_str = self.headers.get("content-length", 0)
        content_length = int(content_length_as_str)

        if not content_length:
            return ""

        payload_as_bytes = self.rfile.read(content_length)
        payload = to_str(payload_as_bytes)

        return payload
