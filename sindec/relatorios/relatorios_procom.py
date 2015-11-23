from sindec.models import Procom


def relatorio_qtd_procom_por_regiao(context=None):
    if context is None:
        context = dict()
    regioes = [str(x[1]) for x in Procom.CHOICES_REGIAO]
    qtd_por_regioes = [{
        "name": "Quantidade de Procom",
        "data": [Procom.objects.filter(regiao=r[0]).count() for r in Procom.CHOICES_REGIAO]
    }]
    context["categorias"] = regioes
    context["conjuntos"] = qtd_por_regioes
    context["titulo_grafico"] = "Procom x Região"

    return context

