from django.urls import path

from applications.blog.apps import BlogConfig
from applications.blog.views import IndexView, NewPostView, DeletePostView, UpdatePostView

app_name = BlogConfig.label

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("new/", NewPostView.as_view(), name="new-post"),
    path("<int:pk>/delete/", DeletePostView.as_view(), name="delete-post"),
    path("<int:pk>/update/", UpdatePostView.as_view(), name="update-post"),
]
