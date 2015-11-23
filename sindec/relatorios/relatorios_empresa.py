from sindec.models import CNAE
from django.db.models import Count


def relatorio_top_10_qtd_empresa_por_cnae(context):
    if context is None:
        context = dict()
    top_10_cnae = list()
    qtd_empresa = list()
    qtd_empresa_data = list()
    for c in CNAE.objects.annotate(num_empresas=Count('empresa')).order_by('-num_empresas')[:10]:
        top_10_cnae.append(c.descricao_cnae)
        qtd_empresa_data.append(c.num_empresas)
    qtd_empresa.append({
        "name": "CNAE",
        "data": qtd_empresa_data
    })
    context["categorias"] = top_10_cnae
    context["conjuntos"] = qtd_empresa
    context["titulo_grafico"] = "TOP 10 CNAEs por Empresa"
    context["metrica"] = "Empresas"
    context["labely"] = "Quantidade de Empresas"


    return context
