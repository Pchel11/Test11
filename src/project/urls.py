from pathlib import Path

from django.contrib import admin
from django.http import HttpResponse, HttpRequest
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt


def main_style(request: HttpRequest):
    style = Path(__file__).parent.parent.parent / "static" / "styles" / "style.css"
    with style.open("r") as f:
        content = f.read()
    return HttpResponse(content, content_type="text/css")


def bg(request: HttpRequest):
    img = Path(__file__).parent.parent.parent / "static" / "images" / "back.jpg"
    with img.open("rb") as f:
        content = f.read()
    return HttpResponse(content, content_type="image/jpg")


def handle_hello(request: HttpRequest):
    hello_html = Path(__file__).parent.parent.parent / "static" / "hello.html"
    with hello_html.open("r") as f:
        content = f.read()
        # content = content.format(request.POST)
    return HttpResponse(content)


def handle_hello_style(request: HttpRequest):
    style = Path(__file__).parent.parent.parent / "static" / "styles" / "theme_light.css"
    with style.open("r") as f:
        content = f.read()
    return HttpResponse(content, content_type="text/css")


def handle_hello_redirect(request: HttpRequest):
    return HttpResponse()


@csrf_exempt
def handle_hello_update(request: HttpRequest):
    print(request.POST)

    return HttpResponse()


def handle_theme(request: HttpRequest):
    return HttpResponse()


def handle_hello_reset(request: HttpRequest):
    return HttpResponse()


def handle_static(request: HttpRequest):
    return HttpResponse()


def get_form_data(request: HttpRequest):
    return HttpResponse()


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("applications.home.urls")),
    path("style", main_style),
    path("bg", bg),
    path("hello/style/", handle_hello_style),
    path("hello/redirect/", handle_hello_redirect),
    path("switch-theme/", handle_theme),
    path("hello/", include("applications.hello.urls"))

]
