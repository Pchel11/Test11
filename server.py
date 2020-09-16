import os
import traceback

from http.server import SimpleHTTPRequestHandler
from custom_types import HttpRequest
from custom_types import User
from errors import MethodNotAllowed
from errors import NotFound
from utils import read_static, get_form_data
from utils import to_bytes
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
            "/hello-reset/": [self.handle_hello_reset, []],
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

    def get_session(self):
        cookie = self.headers.get("Cookie", "")
        qs = cookie.split(":")
        session = qs[0]
        if not session:
            return ""
        return session

    @staticmethod
    def generate_new_session() -> str:
        return os.urandom(8).hex()

    def handle_hello(self, request: HttpRequest):
        if request.method != "get":
            raise MethodNotAllowed

        session = self.get_session()

        if not session:
            session = self.generate_new_session()
            user = User.build(" ")
            content = render_hello_page(user, user)
            self.respond(content, session=session)
            return

        query = load_user_data(str(session))
        user = User.build(query)

        content = render_hello_page(user, user)

        self.respond(content)

    def handle_hello_update(self, request: HttpRequest):
        if request.method != "post":
            raise MethodNotAllowed

        form_data = get_form_data(self.headers, self.rfile)
        new_user = User.build(form_data)

        session = self.get_session() or self.generate_new_session()

        if not new_user.errors:
            save_user_data(form_data, session)
            self.redirect("/hello")
            return

        saved_data = load_user_data(self.get_session())
        saved_user = User.build(saved_data)

        hello_page = render_hello_page(new_user, saved_user)

        self.respond(hello_page)

    def handle_hello_reset(self):
        session = self.get_session()
        save_user_data(" ", session)
        self.redirect("/hello")

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

    def respond(self, message, code=200, content_type="text/html", session=None):
        payload = to_bytes(message)

        self.send_response(code)
        self.send_header("Content-type", content_type)
        self.send_header("Content-length", str(len(payload)))
        if session:
            self.send_header("Set-Cookie", session)
        self.end_headers()
        self.wfile.write(payload)

    def redirect(self, to):
        self.send_response(302)
        self.send_header("Location", to)
        self.end_headers()
