from django.http.response import Http404
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
        context = relatorios_reclamacoes.relatorio_reclamacoes_abertas_por_mes(context=context, ano_final=2009,
                                                                               ano_inicial=2007)
        return context

    @method_decorator(login_required(login_url=reverse_lazy("login")))
    def dispatch(self, *args, **kwargs):
        return super(DashboardRequestView, self).dispatch(*args, **kwargs)


class RelatorioReclamacoesAbertasPorMesRequestView(TemplateView):
    http_method_names = ['get', ]
    template_name = 'relatorios/relatorio_reclamacoes_abertas_por_mes.html'

    def get_context_data(self, ano_inicial=2009, ano_final=2009, **kwargs):
        assert int(ano_inicial) and int(ano_final), Http404()
        if ano_inicial > ano_final:
            ano_inicial, ano_final = ano_final, ano_inicial
        context = super(RelatorioReclamacoesAbertasPorMesRequestView, self).get_context_data(**kwargs)
        context = relatorios_reclamacoes.relatorio_reclamacoes_abertas_por_mes(context=context,
                                                                               ano_final=int(ano_final),
                                                                               ano_inicial=int(ano_inicial))
        return context

    @method_decorator(login_required(login_url=reverse_lazy("login")))
    def dispatch(self, *args, **kwargs):
        return super(RelatorioReclamacoesAbertasPorMesRequestView, self).dispatch(*args, **kwargs)
