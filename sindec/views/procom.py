from django.http.response import Http404
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy


class DashboardRequestView(TemplateView):
    http_method_names = ['get', ]
    template_name = "procom/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardRequestView, self).get_context_data(**kwargs)
        # context["tcol"] = ["Coluna {}".format(x) for x in range(colunas)]
        # context["trd"] = [[x for x in range(counas)] for y in range(qtd_dados)]
        return context

    @method_decorator(login_required(login_url=reverse_lazy("login")))
    def dispatch(self, *args, **kwargs):
        return super(DashboardRequestView, self).dispatch(*args, **kwargs)
