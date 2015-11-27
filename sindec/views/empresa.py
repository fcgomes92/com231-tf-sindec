from django.http import HttpResponseRedirect, HttpResponse
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView, View
from django.contrib.auth.decorators import login_required
from sindec.models import Empresa, CNAE
from sindec.utils import strings


class EmpresaAddRequestView(TemplateView):
    http_method_names = ["get", "post", ]
    template_name = "empresa/empresa_add.html"
    model_fields = Empresa._meta.get_all_field_names()

    def get_context_data(self, **kwargs):
        context = super(EmpresaAddRequestView, self).get_context_data(**kwargs)
        context["cnaes"] = CNAE.objects.all()
        return context

    def post(self, request, *args, **kwargs):

        values = dict()

        print(self.model_fields)

        for pk, pv in request.POST.items():
            if pk in self.model_fields:
                values[pk] = pv

        print(values)

        try:
            e = Empresa(**values)
            # [:7] or [:-6]
            e.cnpj_radical = str(values["cnpj"])[:-6]
            e.save()
            messages.add_message(request=request, level=messages.SUCCESS, message=strings.EMPRESA_ADD_SUCC)
        except Exception as e:
            print(e)
            messages.add_message(request=request, level=messages.ERROR, message=strings.EMPRESA_ADD_ERR)
        return HttpResponse()

    @method_decorator(login_required(login_url=reverse_lazy("login")))
    def dispatch(self, request, *args, **kwargs):
        return super(EmpresaAddRequestView, self).dispatch(request, *args, **kwargs)


class EmpresaListRequestView(TemplateView):
    http_method_names = ["get", ]
    template_name = "empresa/empresa_list.html"

    def get_context_data(self, **kwargs):
        context = super(EmpresaListRequestView, self).get_context_data(**kwargs)
        context["empresas"] = Empresa.objects.all()
        return context

    @method_decorator(login_required(login_url=reverse_lazy("login")))
    def dispatch(self, request, *args, **kwargs):
        return super(EmpresaListRequestView, self).dispatch(request, *args, **kwargs)


class EmpresaUpdateRequestView(TemplateView):
    http_method_names = ["get", "post", ]
    template_name = "empresa/empresa_update.html"
    model_fields = Empresa._meta.get_all_field_names()

    def get_context_data(self, empresa_id=None, **kwargs):
        if empresa_id is None:
            return HttpResponseRedirect(url=reverse_lazy("dashboard"))
        else:
            context = super(EmpresaUpdateRequestView, self).get_context_data(**kwargs)
            context["empresa"] = Empresa.objects.get(pk=int(empresa_id))
            context["cnaes"] = CNAE.objects.all()
            return context

    def post(self, request, empresa_id=None, *args, **kwargs):

        values = dict()

        for pk, pv in request.POST.items():
            if pk in self.model_fields:
                values[pk] = pv

        try:
            e = Empresa.objects.get(pk=empresa_id)
            e.razao_social_sindec = values["razao_social_sindec"]
            e.nome_fantasia_sindec = values["nome_fantasia_sindec"]
            e.razao_social_rfb = values["razao_social_rfb"]
            e.nome_fantasia_rfb = values["nome_fantasia_rfb"]
            e.cnae_id = values["cnae_id"]
            e.save()
            messages.add_message(request=request, level=messages.SUCCESS, message=strings.EMPRESA_UPD_SUCC)
        except Exception as e:
            print(e)
            messages.add_message(request=request, level=messages.ERROR, message=strings.EMPRESA_UPD_ERR)
        return HttpResponse()

    @method_decorator(login_required(login_url=reverse_lazy("login")))
    def dispatch(self, request, *args, **kwargs):
        return super(EmpresaUpdateRequestView, self).dispatch(request, *args, **kwargs)
