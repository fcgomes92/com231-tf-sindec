from django.conf.urls import url
from sindec.views import csv as sindec_csv
from sindec.views import user as sindec_user
from sindec.views import home as sindec_home
from sindec.views import procom as sindec_procom

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
    url(r'^relatorio/reclamacoes/abertas/mes/(?P<ano_inicial>[0-9]{4})/(?P<ano_final>[0-9]{4})/$',
        sindec_procom.RelatorioReclamacoesAbertasPorMesRequestView.as_view(), name="relatorio_reclamacoes_abertas_mes"),
    # url(r'^register/$', sindec_user.RegisterRequestView.as_view(), name="register"),
    # url(r'^register/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', sindec_user.RegisterConfirmRequest.as_view(),
    #     name='register_confirm'),
]
