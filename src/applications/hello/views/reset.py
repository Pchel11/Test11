from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import Form
from django.urls import reverse_lazy
from django.views.generic import FormView


class ResetView(LoginRequiredMixin, FormView):
    form_class = Form
    http_method_names = ["post"]
    success_url = reverse_lazy("hello:index")

    def form_valid(self, form):
        self.request.session.clear()

        return super().form_valid(form)