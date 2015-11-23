from django.views.generic import TemplateView


class HomeRequestView(TemplateView):
    http_method_names = ['get', ]
    template_name = "home.html"
