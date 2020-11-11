from django.urls import reverse_lazy
from django.views.generic import CreateView

from applications.blog.models import Post


class NewPostView(CreateView):
    fields = [Post.title.field.name, Post.content.field.name]
    model = Post
    success_url = reverse_lazy("blog:index")
    extra_context = {
        "action_name": "Create Post",
        "action_url": reverse_lazy("blog:new-post"),
    }
