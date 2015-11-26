from django.http import HttpResponseRedirect, HttpResponse
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView, View
from django.contrib.auth.decorators import login_required
from sindec.models import Problema
from sindec.utils import strings


class ProblemaAddRequestView(TemplateView):
    http_method_names = ["get", "post", ]
    template_name = "problema/problema_add.html"

    def post(self, request, *args, **kwargs):
        problema_descricao = request.POST.get("problema_descricao", None)
        if problema_descricao is not None:
            p = Problema(descricao_problema=problema_descricao)
            p.save()
            messages.add_message(request=request, level=messages.SUCCESS, message=strings.PROBLEMA_ADD_SUCC)
        else:
            messages.add_message(request=request, level=messages.ERROR, message=strings.PROBLEMA_ADD_ERR)
        return HttpResponse()

    @method_decorator(login_required(login_url=reverse_lazy("login")))
    def dispatch(self, request, *args, **kwargs):
        return super(ProblemaAddRequestView, self).dispatch(request, *args, **kwargs)


class ProblemaListRequestView(TemplateView):
    http_method_names = ["get", ]
    template_name = "problema/problema_list.html"

    def get_context_data(self, **kwargs):
        context = super(ProblemaListRequestView, self).get_context_data(**kwargs)
        context["problemas"] = Problema.objects.all()
        return context

    @method_decorator(login_required(login_url=reverse_lazy("login")))
    def dispatch(self, request, *args, **kwargs):
        return super(ProblemaListRequestView, self).dispatch(request, *args, **kwargs)


class ProblemaUpdateRequestView(TemplateView):
    http_method_names = ["get", "post", ]
    template_name = "problema/problema_update.html"

    def get_context_data(self, problema_id=None, **kwargs):
        if problema_id is None:
            return HttpResponseRedirect(url=reverse_lazy("dashboard"))
        else:
            context = super(ProblemaUpdateRequestView, self).get_context_data(**kwargs)
            context["problema"] = Problema.objects.get(pk=int(problema_id))
            return context

    def post(self, request, problema_id=None, *args, **kwargs):
        problema_descricao = request.POST.get("problema_descricao", None)
        if None not in []:
            p = Problema.objects.get(pk=problema_id)
            p.descricao_problema = problema_descricao
            p.save()
            messages.add_message(request=request, level=messages.SUCCESS, message=strings.PROBLEMA_UPD_SUCC)
        else:
            messages.add_message(request=request, level=messages.ERROR, message=strings.PROBLEMA_UPD_ERR)
        return HttpResponse()

    @method_decorator(login_required(login_url=reverse_lazy("login")))
    def dispatch(self, request, *args, **kwargs):
        return super(ProblemaUpdateRequestView, self).dispatch(request, *args, **kwargs)
