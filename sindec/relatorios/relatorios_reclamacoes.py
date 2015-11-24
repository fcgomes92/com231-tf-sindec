from sindec.models import Assunto, Reclamacao, Problema
from django.db.models import Count
from django.utils import timezone


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


def relatorio_reclamacoes_problemas_top_10_atendidas_ou_nao_atendidas(context, atendidas=True):
    reclamacoes = list()
    qtd_reclamacoes = list()
    qtd_reclamacoes_data = list()
    for p in Reclamacao.objects.values('atendida', 'problema__descricao_problema').annotate(
            num_reclamacoes=Count('atendida')).filter(atendida=atendidas).order_by('-num_reclamacoes')[:10]:
        reclamacoes.append(p.get("problema__descricao_problema", ""))
        qtd_reclamacoes_data.append(p.get("num_reclamacoes", ""))
    qtd_reclamacoes.append({
        "name": "Reclamações {}".format("Atendidas" if atendidas else "Não Atendidas"),
        "data": qtd_reclamacoes_data
    })
    context["categorias"] = reclamacoes
    context["conjuntos"] = qtd_reclamacoes
    context["titulo_grafico"] = "TOP 10 Reclamações {} - Por Problema".format(
        "Atendidas" if atendidas else "Não Atendidas")
    context["metrica"] = "Reclamações"
    context["labely"] = "Quantidade de Reclamações {}".format("Atendidas" if atendidas else "Não Atendidas")

    return context


def relatorio_reclamacoes_assuntos_top_10_atendidas_ou_nao_atendidas(context, atendidas=True):
    reclamacoes = list()
    qtd_reclamacoes = list()
    qtd_reclamacoes_data = list()
    for p in Reclamacao.objects.values('atendida', 'assunto__descricao_assunto').annotate(
            num_reclamacoes=Count('atendida')).filter(atendida=atendidas).order_by('-num_reclamacoes')[:10]:
        reclamacoes.append(p.get("assunto__descricao_assunto", ""))
        qtd_reclamacoes_data.append(p.get("num_reclamacoes", ""))
    qtd_reclamacoes.append({
        "name": "Reclamações {}".format("Atendidas" if atendidas else "Não Atendidas"),
        "data": qtd_reclamacoes_data
    })
    context["categorias"] = reclamacoes
    context["conjuntos"] = qtd_reclamacoes
    context["titulo_grafico"] = "TOP 10 Reclamações {} - Por Assunto".format(
        "Atendidas" if atendidas else "Não Atendidas")
    context["metrica"] = "Reclamações"
    context["labely"] = "Quantidade de Reclamações {}".format("Atendidas" if atendidas else "Não Atendidas")

    return context


def relatorio_reclamacoes_empresas_geral_atendidas_e_nao(context, quantidade=10):
    reclamacoes = list()
    qtd_reclamacoes = list()
    qtd_reclamacoes_total = list()
    qtd_reclamacoes_atendida = list()
    qtd_reclamacoes_natendida = list()
    for p in Reclamacao.objects.values('empresa', 'empresa__razao_social_sindec').annotate(
            num_reclamacoes=Count('atendida')).order_by('-num_reclamacoes')[:quantidade]:
        reclamacoes_an = Reclamacao.objects.filter(empresa=p.get("empresa")).values('atendida').annotate(
            num_reclamacoes=Count('atendida')).order_by('atendida')
        reclamacoes.append(p.get("empresa__razao_social_sindec", ""))
        qtd_reclamacoes_total.append(p.get("num_reclamacoes", ""))
        qtd_reclamacoes_natendida.append(reclamacoes_an[0].get("num_reclamacoes"))
        qtd_reclamacoes_atendida.append(reclamacoes_an[1].get("num_reclamacoes"))
    qtd_reclamacoes.append({
        "name": "Total de Reclamações",
        "data": qtd_reclamacoes_total
    })
    qtd_reclamacoes.append({
        "name": "Total de Reclamações - Não Atendidas",
        "data": qtd_reclamacoes_natendida
    })
    qtd_reclamacoes.append({
        "name": "Total de Reclamações - Atendidas",
        "data": qtd_reclamacoes_atendida
    })
    context["categorias"] = reclamacoes
    context["conjuntos"] = qtd_reclamacoes
    context["titulo_grafico"] = "TOP {} Reclamações Por Empresa".format(quantidade)
    context["metrica"] = "Reclamações"
    context["labely"] = "Quantidade de Reclamações Por Empresa"

    return context


def relatorio_reclamacoes_abertas_por_mes(context, ano_inicial=2009, ano_final=2009):
    if context is None:
        context = dict()
    meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez', ]
    reclamacoes_data = [0 for i in meses]
    qtd_reclamacoes = list()

    for r in Reclamacao.objects.values('data_abertura').annotate(num_reclamacoes=Count('data_abertura')) \
            .filter(data_abertura__gt=timezone.datetime(year=ano_inicial, month=1, day=1)) \
            .filter(data_abertura__lt=timezone.datetime(year=ano_final, month=12, day=30)):
        reclamacoes_data[r.get("data_abertura").month - 1] += r.get('num_reclamacoes')

    qtd_reclamacoes.append({
        "name": "Abertura de Reclamações",
        "data": reclamacoes_data
    })

    reclamacoes_data = [0 for i in meses]

    for r in Reclamacao.objects.values('data_fechamento').annotate(num_reclamacoes=Count('data_fechamento')) \
            .filter(data_abertura__gt=timezone.datetime(year=ano_inicial, month=1, day=1)) \
            .filter(data_abertura__lt=timezone.datetime(year=ano_final, month=12, day=30)):
        reclamacoes_data[r.get("data_fechamento").month - 1] += r.get('num_reclamacoes')

    qtd_reclamacoes.append({
        "name": "Fechamento de Reclamações",
        "data": reclamacoes_data
    })

    context["categorias"] = meses
    context["conjuntos"] = qtd_reclamacoes
    context["titulo_grafico"] = "Reclamações Abertas de {} a {}".format(ano_inicial, ano_final)
    context["metrica"] = "Reclamações"
    context["labely"] = "Quantidade de Reclamações Abertas"

    return context


# Relatórios em pizza
def relatorio_reclamacoes_atendidas(context):
    if context is None:
        context = dict()
    reclamacoes = list()
    qtd_reclamacoes = list()
    for r in Reclamacao.objects.values('atendida').annotate(num_reclamacoes=Count('atendida')).order_by(
            '-num_reclamacoes'):
        qtd_reclamacoes.append({
            "name": "Atendidas" if r.get("atendida") else "Não Atendidas",
            "data": r.get("num_reclamacoes")
        })
    context["conjuntos"] = qtd_reclamacoes
    context["titulo_grafico"] = "TOP 10 Assuntos por Reclamação"
    context["metrica"] = "Reclamações"
    context["labely"] = "Quantidade de Reclamações"

    return context
