from django.http import HttpResponseRedirect, HttpResponse
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView, View
from django.contrib.auth.decorators import login_required
from sindec.models import CNAE
from sindec.utils import strings


class CNAEAddRequestView(TemplateView):
    http_method_names = ["get", "post", ]
    template_name = "cnae/cnae_add.html"

    def post(self, request, *args, **kwargs):
        cnae_descricao = request.POST.get("cnae_descricao", None)
        if cnae_descricao is not None:
            p = CNAE(descricao_cnae=cnae_descricao)
            p.save()
            messages.add_message(request=request, level=messages.SUCCESS, message=strings.CNAE_ADD_SUCC)
        else:
            messages.add_message(request=request, level=messages.ERROR, message=strings.CNAE_ADD_ERR)
        return HttpResponse()

    @method_decorator(login_required(login_url=reverse_lazy("login")))
    def dispatch(self, request, *args, **kwargs):
        return super(CNAEAddRequestView, self).dispatch(request, *args, **kwargs)


class CNAEListRequestView(TemplateView):
    http_method_names = ["get", ]
    template_name = "cnae/cnae_list.html"

    def get_context_data(self, **kwargs):
        context = super(CNAEListRequestView, self).get_context_data(**kwargs)
        context["cnaes"] = CNAE.objects.all()
        return context

    @method_decorator(login_required(login_url=reverse_lazy("login")))
    def dispatch(self, request, *args, **kwargs):
        return super(CNAEListRequestView, self).dispatch(request, *args, **kwargs)


class CNAEUpdateRequestView(TemplateView):
    http_method_names = ["get", "post", ]
    template_name = "cnae/cnae_update.html"

    def get_context_data(self, cnae_id=None, **kwargs):
        if cnae_id is None:
            return HttpResponseRedirect(url=reverse_lazy("dashboard"))
        else:
            context = super(CNAEUpdateRequestView, self).get_context_data(**kwargs)
            context["cnae"] = CNAE.objects.get(pk=int(cnae_id))
            return context

    def post(self, request, cnae_id=None, *args, **kwargs):
        cnae_descricao = request.POST.get("cnae_descricao", None)
        if None not in []:
            p = CNAE.objects.get(pk=cnae_id)
            p.descricao_cnae = cnae_descricao
            p.save()
            messages.add_message(request=request, level=messages.SUCCESS, message=strings.CNAE_UPD_SUCC)
        else:
            messages.add_message(request=request, level=messages.ERROR, message=strings.CNAE_UPD_ERR)
        return HttpResponse()

    @method_decorator(login_required(login_url=reverse_lazy("login")))
    def dispatch(self, request, *args, **kwargs):
        return super(CNAEUpdateRequestView, self).dispatch(request, *args, **kwargs)
