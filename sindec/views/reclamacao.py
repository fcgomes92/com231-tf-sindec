from django.utils.decorators import method_decorator
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse
from django.utils import timezone
import re
from sindec.models import Empresa, Assunto, Problema, Consumidor, Reclamacao
from sindec.utils import strings


class ReclamacaoAddRequestView(TemplateView):
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


def str_date_to_iso_format(dt="23/06/1992", splt="/"):
    dt = dt.split(splt)
    return "{}-{}-{}".format(dt[2], dt[1], dt[0])
