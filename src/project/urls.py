from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("applications.home.urls")),
    path("b/", include("applications.blog.urls")),
    path("hello/", include("applications.hello.urls")),
    path("tg-bots/", include("applications.bots.urls")),
]
