from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from applications.blog.models import Post


class IndexView(LoginRequiredMixin, ListView):
    template_name = "blog/index.html"
    queryset = Post.objects.filter(visible=True)
