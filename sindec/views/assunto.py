from django.http import HttpResponseRedirect, HttpResponse
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView, View
from django.contrib.auth.decorators import login_required
from sindec.models import Assunto
from sindec.utils import strings


class AssuntoAddRequestView(TemplateView):
    http_method_names = ["get", "post", ]
    template_name = "assunto/assunto_add.html"

    def post(self, request, *args, **kwargs):
        assunto_descricao = request.POST.get("assunto_descricao", None)
        if assunto_descricao is not None:
            p = Assunto(descricao_assunto=assunto_descricao)
            p.save()
            messages.add_message(request=request, level=messages.SUCCESS, message=strings.ASSUNTO_ADD_SUCC)
        else:
            messages.add_message(request=request, level=messages.ERROR, message=strings.ASSUNTO_ADD_ERR)
        return HttpResponse()

    @method_decorator(login_required(login_url=reverse_lazy("login")))
    def dispatch(self, request, *args, **kwargs):
        return super(AssuntoAddRequestView, self).dispatch(request, *args, **kwargs)


class AssuntoListRequestView(TemplateView):
    http_method_names = ["get", ]
    template_name = "assunto/assunto_list.html"

    def get_context_data(self, **kwargs):
        context = super(AssuntoListRequestView, self).get_context_data(**kwargs)
        context["assuntos"] = Assunto.objects.all()
        return context

    @method_decorator(login_required(login_url=reverse_lazy("login")))
    def dispatch(self, request, *args, **kwargs):
        return super(AssuntoListRequestView, self).dispatch(request, *args, **kwargs)


class AssuntoUpdateRequestView(TemplateView):
    http_method_names = ["get", "post", ]
    template_name = "assunto/assunto_update.html"

    def get_context_data(self, assunto_id=None, **kwargs):
        if assunto_id is None:
            return HttpResponseRedirect(url=reverse_lazy("dashboard"))
        else:
            context = super(AssuntoUpdateRequestView, self).get_context_data(**kwargs)
            context["assunto"] = Assunto.objects.get(pk=int(assunto_id))
            return context

    def post(self, request, assunto_id=None, *args, **kwargs):
        assunto_descricao = request.POST.get("assunto_descricao", None)
        if None not in []:
            p = Assunto.objects.get(pk=assunto_id)
            p.descricao_assunto = assunto_descricao
            p.save()
            messages.add_message(request=request, level=messages.SUCCESS, message=strings.ASSUNTO_UPD_SUCC)
        else:
            messages.add_message(request=request, level=messages.ERROR, message=strings.ASSUNTO_UPD_ERR)
        return HttpResponse()

    @method_decorator(login_required(login_url=reverse_lazy("login")))
    def dispatch(self, request, *args, **kwargs):
        return super(AssuntoUpdateRequestView, self).dispatch(request, *args, **kwargs)
