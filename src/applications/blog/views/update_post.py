from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from applications.blog.models import Post


class UpdatePostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    fields = [Post.title.field.name, Post.content.field.name]
    model = Post
    success_url = reverse_lazy("blog:index")

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx.update(
            {
                "action_name": "Update Post",
                "action_url": reverse_lazy(
                    "blog:update-post",
                    kwargs={
                        "pk": self.object.pk,
                    },
                ),
            }
        )

        return ctx
