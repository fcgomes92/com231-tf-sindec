from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from sindec.relatorios import relatorios_procom, relatorios_empresa, relatorios_reclamacoes


class DashboardRequestView(TemplateView):
    http_method_names = ['get', ]
    template_name = "procom/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardRequestView, self).get_context_data(**kwargs)
        context = relatorios_reclamacoes.relatorio_reclamacoes_empresas_geral_atendidas_e_nao(context)
        return context

    @method_decorator(login_required(login_url=reverse_lazy("login")))
    def dispatch(self, *args, **kwargs):
        return super(DashboardRequestView, self).dispatch(*args, **kwargs)
