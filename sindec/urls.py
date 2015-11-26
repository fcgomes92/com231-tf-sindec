from django.conf.urls import url
from sindec.views import csv as sindec_csv
from sindec.views import user as sindec_user
from sindec.views import home as sindec_home
from sindec.views import procom as sindec_procom
from sindec.views import reclamacao as sindec_reclamacao
from sindec.views import problema as sindec_problema

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
    url(r'^reclamacao/add/$', sindec_reclamacao.ReclamacaoAddRequestView.as_view(), name="reclamacao_add"),
    url(r'^reclamacao/list/$', sindec_reclamacao.ReclamacaoListRequestView.as_view(), name="reclamacao_list"),
    url(r'^reclamacao/search/$', sindec_reclamacao.ReclamacaoSearchRequest.as_view(), name="reclamacao_search"),
    url(r'^reclamacao/update/(?P<reclamacao_id>[0-9]+)/(?P<reclamacao_atendida>[0-1])/$',
        sindec_reclamacao.ReclamacaoUpdateRequest.as_view(), name="reclamacao_update"),
    url(r'^problema/add/$', sindec_problema.ProblemaAddRequestView.as_view(), name="problema_add"),
    url(r'^problema/list/$', sindec_problema.ProblemaListRequestView.as_view(), name="problema_list"),
    url(r'^problema/update/(?P<problema_id>[0-9]+)/$',
        sindec_problema.ProblemaUpdateRequestView.as_view(), name="problema_update"),

    url(r'^relatorio/reclamacoes/abertas/mes/(?P<ano_inicial>[0-9]{4})/(?P<ano_final>[0-9]{4})/$',
        sindec_procom.RelatorioReclamacoesAbertasPorMesRequestView.as_view(), name="relatorio_reclamacoes_abertas_mes"),
    # url(r'^register/$', sindec_user.RegisterRequestView.as_view(), name="register"),
    # url(r'^register/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', sindec_user.RegisterConfirmRequest.as_view(),
    #     name='register_confirm'),
]

# DONE: CRUD Reclamação
# TODO: CRUD Empresa
# TODO: CRUD Assunto
# TODO: CRUD Problema
# TODO: CRUD CNAE
