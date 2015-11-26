from django.http.response import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView, View
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse
from django.utils import timezone
import re
from rest_framework.renderers import JSONRenderer
from sindec.models import Empresa, Assunto, Problema, Consumidor, Reclamacao
from sindec.utils import strings
from sindec.serializers import ReclamacaoSerializer


class ReclamacaoAddRequestView(TemplateView):
    http_method_names = ["get", "post", ]
    template_name = "reclamacao/reclamacao_add.html"

    def get_context_data(self, **kwargs):
        context = super(ReclamacaoAddRequestView, self).get_context_data(**kwargs)
        context["empresas"] = Empresa.objects.all().values('pk', 'razao_social_sindec', 'cnpj')
        context["assuntos"] = Assunto.objects.all().values('pk', 'descricao_assunto')
        context["problemas"] = Problema.objects.all().values('pk', 'descricao_problema')
        context["generos"] = Consumidor.CHOICES_GENDER
        context["fes"] = Consumidor.CHOICES_FE
        return context

    def post(self, request, *args, **kwargs):
        reclamador_data_nascimento = request.POST.get("reclamador_data_nascimento", None)
        reclamador_cep = request.POST.get("reclamador_cep", None)
        reclamador_genero = request.POST.get("reclamador_genero", None)
        reclamador_faixa_etaria = request.POST.get("reclamador_faixa_etaria", None)
        empresa = request.POST.get("empresa", None)
        problema = request.POST.get("problema", None)
        assunto = request.POST.get("assunto", None)

        if None not in [empresa, problema, assunto, reclamador_genero, reclamador_faixa_etaria]:
            if re.match("[0-9]{2}/[0-9]{2}/[0-9]{2}", reclamador_data_nascimento) is not None:
                reclamador_data_nascimento = str_date_to_iso_format(reclamador_data_nascimento, "/")
            try:
                reclamador = Consumidor(
                    sexo=reclamador_genero,
                    data_nascimento=reclamador_data_nascimento,
                    faixa_etaria=reclamador_faixa_etaria,
                    cep_consumidor=reclamador_cep
                )

                reclamador.save()

                td = timezone.now()

                r = Reclamacao(
                    reclamador=reclamador,
                    registrador_id=request.user.pk,
                    empresa_id=empresa,
                    ano=str(td.year),
                    assunto_id=assunto,
                    problema_id=problema,
                    data_abertura=td.isoformat(),
                    data_fechamento=None,
                    atendida=False,
                )
                r.save()
                messages.add_message(request=request, level=messages.SUCCESS, message=strings.RECLAMACAO_ADD_SUCC)

            except Exception as e:
                print(e)
                messages.add_message(request=request, level=messages.ERROR, message=strings.RECLAMACAO_ADD_ERR)

        else:
            messages.add_message(request=request, level=messages.ERROR, message=strings.RECLAMACAO_ADD_ERR)

        return HttpResponse()

    @method_decorator(login_required(login_url=reverse_lazy("login")))
    def dispatch(self, request, *args, **kwargs):
        return super(ReclamacaoAddRequestView, self).dispatch(request, *args, **kwargs)


class ReclamacaoListRequestView(TemplateView):
    http_method_names = ["get", ]
    template_name = "reclamacao/reclamacao_list.html"

    def get_context_data(self, **kwargs):
        context = super(ReclamacaoListRequestView, self).get_context_data(**kwargs)
        context["empresas"] = Empresa.objects.all().values('pk', 'razao_social_sindec', 'cnpj')
        context["assuntos"] = Assunto.objects.all().values('pk', 'descricao_assunto')
        context["problemas"] = Problema.objects.all().values('pk', 'descricao_problema')
        context["generos"] = Consumidor.CHOICES_GENDER
        context["fes"] = Consumidor.CHOICES_FE
        return context

    @method_decorator(login_required(login_url=reverse_lazy("login")))
    def dispatch(self, request, *args, **kwargs):
        return super(ReclamacaoListRequestView, self).dispatch(request, *args, **kwargs)


class ReclamacaoSearchRequest(View):
    http_method_names = ["get", ]
    form_fields = ['assunto_id', 'reclamador__data_nascimento', 'reclamador__cep__consumidor',
                   'reclamador__faixa_etaria', 'data_abertura__gte', 'empresa_id', 'reclamador__sexo', 'problema_id',
                   'data_abertura__lte']

    def get(self, request, *args, **kwargs):
        filters = dict()
        # filters["reclamador_id"] = request.user.pk

        # pfk = possible filter key / pfv = possible filter value
        for pfk, pfv in request.GET.items():
            if pfk in self.form_fields and pfv != "":
                filters[pfk] = pfv

        # print(filters)

        qs = Reclamacao.objects.all().filter(**filters)

        result = JSONRenderer().render(ReclamacaoSerializer(qs, many=True).data)

        # print(result)

        return HttpResponse(content_type="application/json", content=result)

    @method_decorator(login_required(login_url=reverse_lazy("login")))
    def dispatch(self, request, *args, **kwargs):
        return super(ReclamacaoSearchRequest, self).dispatch(request, *args, **kwargs)


def str_date_to_iso_format(dt="23/06/1992", splt="/"):
    dt = dt.split(splt)
    return "{}-{}-{}".format(dt[2], dt[1], dt[0])


class ReclamacaoUpdateRequest(View):
    http_method_names = ["post", ]

    def post(self, request, reclamacao_id, reclamacao_atendida, *args, **kwargs):
        if None not in [reclamacao_id, reclamacao_atendida]:
            try:
                r = Reclamacao.objects.get(id=reclamacao_id)
                r.atendida = bool(int(reclamacao_atendida))
                r.data_fechamento = timezone.now().isoformat()
                r.save()
                messages.add_message(request=request, level=messages.SUCCESS, message=strings.RECLAMACAO_UPD_SUCC)
                result = HttpResponseRedirect(reverse_lazy("dashboard"))
            except Reclamacao.DoesNotExist:
                messages.add_message(request=request, level=messages.ERROR, message=strings.RECLAMACAO_UPD_ERR)
                result = HttpResponseForbidden()
        else:
            messages.add_message(request=request, level=messages.ERROR, message=strings.RECLAMACAO_UPD_ERR)
            result = HttpResponseForbidden()

        return result

    @method_decorator(login_required(login_url=reverse_lazy("login")))
    def dispatch(self, request, *args, **kwargs):
        return super(ReclamacaoUpdateRequest, self).dispatch(request, *args, **kwargs)
