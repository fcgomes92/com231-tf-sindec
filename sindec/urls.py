from django.conf.urls import url
from sindec.views import csv as sindec_csv
from sindec.views import user as sindec_user
from sindec.views import home as sindec_home
from sindec.views import procom as sindec_procom
from sindec.views import reclamacao as sindec_reclamacao
from sindec.views import problema as sindec_problema
from sindec.views import assunto as sindec_assunto
from sindec.views import cnae as sindec_cnae
from sindec.views import empresa as sindec_empresa
from sindec.views import relatorio as sindec_relatorio

urlpatterns = [
    url(r'^csv_init/$', sindec_csv.csv_test, name="dbinti"),
    url(r'^$', sindec_home.HomeRequestView.as_view(), name="home"),
    url(r'^login/$', sindec_user.LoginRequestView.as_view(), name="login"),
    url(r'^logout/$', sindec_user.LogoutRequestView.as_view(), name="logout"),
    url(r'^reset/password/$', sindec_user.PasswordResetRequestView.as_view(), name="reset_password"),
    url(r'^reset/password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        sindec_user.PasswordResetConfirmView.as_view(),
        name='reset_password_confirm'),
    url(r'^dashboard/$', sindec_procom.DashboardRequestView.as_view(), name="dashboard"),
    # URL : Reclamação
    url(r'^reclamacao/add/$', sindec_reclamacao.ReclamacaoAddRequestView.as_view(), name="reclamacao_add"),
    url(r'^reclamacao/list/$', sindec_reclamacao.ReclamacaoListRequestView.as_view(), name="reclamacao_list"),
    url(r'^reclamacao/search/$', sindec_reclamacao.ReclamacaoSearchRequest.as_view(), name="reclamacao_search"),
    url(r'^reclamacao/update/(?P<reclamacao_id>[0-9]+)/(?P<reclamacao_atendida>[0-1])/$',
        sindec_reclamacao.ReclamacaoUpdateRequest.as_view(), name="reclamacao_update"),

    # URL : Problema
    url(r'^problema/add/$', sindec_problema.ProblemaAddRequestView.as_view(), name="problema_add"),
    url(r'^problema/list/$', sindec_problema.ProblemaListRequestView.as_view(), name="problema_list"),
    url(r'^problema/update/(?P<problema_id>[0-9]+)/$',
        sindec_problema.ProblemaUpdateRequestView.as_view(), name="problema_update"),

    # URL : Assunto
    url(r'^assunto/add/$', sindec_assunto.AssuntoAddRequestView.as_view(), name="assunto_add"),
    url(r'^assunto/list/$', sindec_assunto.AssuntoListRequestView.as_view(), name="assunto_list"),
    url(r'^assunto/update/(?P<assunto_id>[0-9]+)/$',
        sindec_assunto.AssuntoUpdateRequestView.as_view(), name="assunto_update"),

    # URL : CNAE
    url(r'^cnae/add/$', sindec_cnae.CNAEAddRequestView.as_view(), name="cnae_add"),
    url(r'^cnae/list/$', sindec_cnae.CNAEListRequestView.as_view(), name="cnae_list"),
    url(r'^cnae/update/(?P<cnae_id>[0-9]+)/$',
        sindec_cnae.CNAEUpdateRequestView.as_view(), name="cnae_update"),

    # URL : Empresa
    url(r'^empresa/add/$', sindec_empresa.EmpresaAddRequestView.as_view(), name="empresa_add"),
    url(r'^empresa/list/$', sindec_empresa.EmpresaListRequestView.as_view(), name="empresa_list"),
    url(r'^empresa/update/(?P<empresa_id>[0-9]+)/$',
        sindec_empresa.EmpresaUpdateRequestView.as_view(), name="empresa_update"),

    # URL : Relatórios
    url(r'^relatorio/reclamacoes/abertas/mes/(?P<ano_inicial>[0-9]{4})/(?P<ano_final>[0-9]{4})/$',
        sindec_relatorio.RelatorioReclamacoesAbertasPorMesRequestView.as_view(),
        name="relatorio_reclamacoes_abertas_mes"),
    url(r'^relatorio/reclamacoes/top10/(?P<ano_inicial>[0-9]{4})/(?P<ano_final>[0-9]{4})/$',
        sindec_relatorio.RelatorioReclamacoesAbertasPorMesRequestView.as_view(),
        name="relatorio_reclamacoes_abertas_mes"),
    url(r'^relatorio/geral/(?P<ano>[0-9]{4})/$',
        sindec_relatorio.RelatorioDoCadastroNacionalDeReclamacoesFundamentadasRequestView.as_view(),
        name="relatorio_geral"),
    # url(r'^register/$', sindec_user.RegisterRequestView.as_view(), name="register"),
    # url(r'^register/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', sindec_user.RegisterConfirmRequest.as_view(),
    #     name='register_confirm'),
]
