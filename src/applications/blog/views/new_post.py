from typing import NamedTuple

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView


from applications.blog.models import Post


# class AuthorT(NamedTuple):
#     author: str


class NewPostView(LoginRequiredMixin, CreateView):
    # def author(self):
    #     author = self.request.user
    #     author = AuthorT(author=author)
    #     return author

    fields = [Post.title.field.name, Post.content.field.name]
    model = Post
    # author = author
    # f = Post.objects.create(author=author)
    # f.save()
    success_url = reverse_lazy("blog:index")
    extra_context = {
        "action_name": "Create Post",
        "action_url": reverse_lazy("blog:new-post"),
    }

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user
