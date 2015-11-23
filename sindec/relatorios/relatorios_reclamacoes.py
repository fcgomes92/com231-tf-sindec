from sindec.models import Assunto, Reclamacao, Problema
from django.db.models import Count


# Relatórios em barra
def relatorio_top_10_assuntos(context):
    if context is None:
        context = dict()
    top_10_assuntos = list()
    qtd_reclamacoes = list()
    qtd_reclamacoes_data = list()
    for a in Assunto.objects.annotate(num_reclamacoes=Count('reclamacao')).order_by('-num_reclamacoes')[:10]:
        top_10_assuntos.append(a.descricao_assunto)
        qtd_reclamacoes_data.append(a.num_reclamacoes)
    qtd_reclamacoes.append({
        "name": "Assuntos",
        "data": qtd_reclamacoes_data
    })
    context["categorias"] = top_10_assuntos
    context["conjuntos"] = qtd_reclamacoes
    context["titulo_grafico"] = "TOP 10 Assuntos por Reclamação"
    context["metrica"] = "Reclamações"
    context["labely"] = "Quantidade de Reclamações"

    return context


def relatorio_top_10_problemas(context):
    if context is None:
        context = dict()
    top_10_problemas = list()
    qtd_reclamacoes = list()
    qtd_reclamacoes_data = list()
    for p in Problema.objects.annotate(num_reclamacoes=Count('reclamacao')).order_by('-num_reclamacoes')[:10]:
        top_10_problemas.append(p.descricao_problema)
        qtd_reclamacoes_data.append(p.num_reclamacoes)
    qtd_reclamacoes.append({
        "name": "Assuntos",
        "data": qtd_reclamacoes_data
    })
    context["categorias"] = top_10_problemas
    context["conjuntos"] = qtd_reclamacoes
    context["titulo_grafico"] = "TOP 10 Assuntos por Reclamação"
    context["metrica"] = "Reclamações"
    context["labely"] = "Quantidade de Reclamações"

    return context

# Relatórios em pizza
def relatorio_reclamacoes_atendidas(context):
    if context is None:
        context = dict()
    reclamacoes = list()
    qtd_reclamacoes = list()
    qtd_reclamacoes_data = list()
    for p in Reclamacao.objects.annotate(num_reclamacoes=Count('atendida')).order_by('-num_reclamacoes')[:10]:
        reclamacoes.append(p.descricao_problema)
        qtd_reclamacoes_data.append(p.num_reclamacoes)
    qtd_reclamacoes.append({
        "name": "Assuntos",
        "data": qtd_reclamacoes_data
    })
    context["categorias"] = reclamacoes
    context["conjuntos"] = qtd_reclamacoes
    context["titulo_grafico"] = "TOP 10 Assuntos por Reclamação"
    context["metrica"] = "Reclamações"
    context["labely"] = "Quantidade de Reclamações"

##
# Reclamações mais atendidas: models.Reclamacao.objects.values('atendida','problema').annotate(num_reclamacoes=Count('atendida')).filter(atendida=True).order_by('-num_reclamacoes')
# Reclamações mais não atendidas: models.Reclamacao.objects.values('atendida','problema').annotate(num_reclamacoes=Count('atendida')).filter(atendida=False).order_by('-num_reclamacoes')
##