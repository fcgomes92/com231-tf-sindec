from sindec.models import Assunto, Reclamacao, Problema, Empresa, CNAE, Consumidor
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

    # Gráfico
    meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez', ]
    reclamacoes_data = [0 for i in meses]
    qtd_reclamacoes = list()

    for r in Reclamacao.objects.values('data_abertura').annotate(num_reclamacoes=Count('data_abertura')) \
            .filter(data_abertura__gte=timezone.datetime(year=ano_inicial, month=1, day=1)) \
            .filter(data_abertura__lte=timezone.datetime(year=ano_final, month=12, day=30)):
        if r.get("data_abertura", None) is not None:
            reclamacoes_data[r.get("data_abertura").month - 1] += r.get('num_reclamacoes')

    qtd_reclamacoes.append({
        "name": "Abertura de Reclamações",
        "data": reclamacoes_data
    })

    # print(reclamacoes_data)

    reclamacoes_data_fechamento = [0 for i in meses]

    for r in Reclamacao.objects.values('data_fechamento').annotate(num_reclamacoes=Count('data_fechamento')) \
            .filter(data_fechamento__gte=timezone.datetime(year=ano_inicial, month=1, day=1)) \
            .filter(data_fechamento__lte=timezone.datetime(year=ano_final, month=12, day=30)):
        if r.get("data_fechamento", ) is not None:
            reclamacoes_data_fechamento[r.get("data_fechamento").month - 1] += r.get('num_reclamacoes')

    # print(reclamacoes_data_fechamento)

    qtd_reclamacoes.append({
        "name": "Fechamento de Reclamações",
        "data": reclamacoes_data_fechamento
    })

    # Table
    # Colunas
    context["categorias"] = meses
    fc = ["Abertas/Fechadas"]
    fc.extend(meses)
    meses = fc
    context["colunas_meses"] = meses
    context["data_row_aberta_fechada"] = qtd_reclamacoes
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


# Relatório de reclamadores
def relatorio_reclamadores(context, ano=2009):
    if context is None:
        context = dict()
    faixas_etarias = Consumidor.CHOICES_FE
    generos = Consumidor.CHOICES_GENDER
    reclamacoes = Reclamacao.objects.filter(ano=ano)
    result = list()

    ## Faixa Etária
    for r in reclamacoes.exclude(reclamador__faixa_etaria=None).values('reclamador__faixa_etaria').annotate(num_reclamacoes=Count('reclamador__faixa_etaria')).order_by('-num_reclamacoes'):
        result.append({
                "name": faixas_etarias[r.get("reclamador__faixa_etaria")][1],
                "data": [r.get("num_reclamacoes",""),],
            })

    context["reclamacoes_por_faixa_etaria_categorias"] = ["Faixa Etária",]
    context["reclamacoes_por_faixa_etaria_header"] = ["Faixa Etária","Reclamações"]
    context["reclamacoes_por_faixa_etaria"] = result
    context["reclamacoes_por_faixa_etaria_labely"] = "Quantidade de Reclamações"
    context["reclamacoes_por_faixa_etaria_titulo"] = "Reclamações por Faixa Etária"

    ## Genero
    result = list()
    for r in reclamacoes.exclude(reclamador__sexo=None).values('reclamador__sexo').annotate(num_reclamacoes=Count('reclamador__sexo')).order_by('-num_reclamacoes'):
        for i in generos:
            if r.get("reclamador__sexo") == i[0]:
                sexo = i[1]
        result.append({
                "name": sexo,
                "data": [r.get("num_reclamacoes",""),],
            })

    context["reclamacoes_por_sexo_categorias"] = ["Sexo",]
    context["reclamacoes_por_sexo_header"] = ["Sexo","Reclamações"]
    context["reclamacoes_por_sexo"] = result
    context["reclamacoes_por_sexo_labely"] = "Quantidade de Reclamações"
    context["reclamacoes_por_sexo_titulo"] = "Reclamações por Sexo"
        

    # Grafico
    ## CEP
    result = list()
    for r in reclamacoes.values('reclamador__cep_consumidor').annotate(num_reclamacoes=Count('reclamador__cep_consumidor')).order_by('-num_reclamacoes'):
        result.append({
                "name": r.get("reclamador__cep_consumidor"),
                "data": [r.get("num_reclamacoes",""),],
            })

    context["reclamacoes_por_cep_categorias"] = ["CEP",]
    context["reclamacoes_por_cep_header"] = ["CEP","Reclamações"]
    context["reclamacoes_por_cep"] = result[:10]
    context["reclamacoes_por_cep_tabela"] = result
    context["reclamacoes_por_cep_labely"] = "Quantidade de Reclamações"
    context["reclamacoes_por_cep_titulo"] = "Reclamações por CEP"


    return context

# Reclamações ao longo do tempo
# Reclamacao.objects.values('ano').annotate(num_reclamacoes=Count('ano')).order_by('-num_reclamacoes')

# Relatório Geral
def relatorio_do_cadastro_nacional_de_reclamacoes_fundamentadas(context=None, ano=2009):
    if context is None:
        context = dict()

    # Dados gerais
    reclamacoes = Reclamacao.objects.filter(ano=ano)

    context["ano"] = ano
    context["reclamacoes"] = reclamacoes
    context["fornecedores"] = Empresa.objects.all()

    # CNAE
    ## Gráfico
    reclamacoes_por_cnae = reclamacoes.values('empresa__cnae', 'empresa__cnae__descricao_cnae').annotate(
        num_reclamacoes=Count('empresa__cnae')).order_by('-num_reclamacoes')[:100]
    top_10_cnae = list()
    qtd_reclamacoes = list()
    qtd_reclamacoes_data = list()
    for c in reclamacoes_por_cnae[:10]:
        top_10_cnae.append(c["empresa__cnae__descricao_cnae"])
        qtd_reclamacoes_data.append(c["num_reclamacoes"])
    qtd_reclamacoes.append({
        "name": "CNAE",
        "data": qtd_reclamacoes_data,
    })

    context["categorias_cnae"] = top_10_cnae
    context["conjuntos_cnae"] = qtd_reclamacoes
    context["titulo_grafico_cnae"] = "TOP 10 CNAE por Reclamações"
    context["metrica_cnae"] = "Reclamações"
    context["labely_cnae"] = "Quantidade de Reclamações"
    ## Table
    qtd_reclamacoes = list()
    top_100_cnae = list()
    for c in reclamacoes_por_cnae:
        top_100_cnae.append(c["empresa__cnae__descricao_cnae"])
        qtd_reclamacoes.append({
            "name": c["empresa__cnae__descricao_cnae"],
            "data": [c["num_reclamacoes"], ]
        })

    context["colunas_cnae"] = ["CNAE", "Quantidade Reclamações", ]
    context["data_row_cnae"] = qtd_reclamacoes

    # Assuntos
    ## Gráfico
    reclamacoes_por_assunto = reclamacoes.values("assunto_id", "assunto__descricao_assunto").annotate(
        num_reclamacoes=Count("assunto_id")).order_by("-num_reclamacoes")[:100]
    top_10_assuntos = list()
    qtd_reclamacoes = list()
    qtd_reclamacoes_data = list()
    for a in reclamacoes_por_assunto[:10]:
        top_10_assuntos.append(a["assunto__descricao_assunto"])
        qtd_reclamacoes_data.append(a["num_reclamacoes"])
    qtd_reclamacoes.append({
        "name": "Assunto",
        "data": qtd_reclamacoes_data,
    })
    context["categorias_assunto"] = top_10_assuntos
    context["conjuntos_assunto"] = qtd_reclamacoes
    context["titulo_grafico_assunto"] = "TOP 10 Assuntos por Reclamação"
    context["metrica_assunto"] = "Reclamações"
    context["labely_assunto"] = "Quantidade de Reclamações"
    ## Table
    qtd_reclamacoes = list()
    top_100_assuntos = list()
    for a in reclamacoes_por_assunto:
        top_100_assuntos.append(a["assunto__descricao_assunto"])
        qtd_reclamacoes.append({
            "name": a["assunto__descricao_assunto"],
            "data": [a["num_reclamacoes"], ]
        })
    context["colunas_assunto"] = ["CNAE", "Quantidade Reclamações", ]
    context["data_row_assunto"] = qtd_reclamacoes

    # Problemas
    ## Gráfico
    reclamacoes_por_problema = reclamacoes.values("problema_id", "problema__descricao_problema").annotate(
        num_reclamacoes=Count("problema_id")).order_by("-num_reclamacoes")[:100]
    top_10_problemas = list()
    qtd_reclamacoes = list()
    qtd_reclamacoes_data = list()
    for a in reclamacoes_por_problema[:10]:
        top_10_problemas.append(a["problema__descricao_problema"])
        qtd_reclamacoes_data.append(a["num_reclamacoes"])
    qtd_reclamacoes.append({
        "name": "Problema",
        "data": qtd_reclamacoes_data,
    })
    context["categorias_problema"] = top_10_problemas
    context["conjuntos_problema"] = qtd_reclamacoes
    context["titulo_grafico_problema"] = "TOP 10 Problemas por Reclamação"
    context["metrica_problema"] = "Reclamações"
    context["labely_problema"] = "Quantidade de Reclamações"
    ## Table
    qtd_reclamacoes = list()
    top_100_problemas = list()
    for a in reclamacoes_por_problema:
        top_100_problemas.append(a["problema__descricao_problema"])
        qtd_reclamacoes.append({
            "name": a["problema__descricao_problema"],
            "data": [a["num_reclamacoes"], ]
        })
    context["colunas_problema"] = ["CNAE", "Quantidade Reclamações", ]
    context["data_row_problema"] = qtd_reclamacoes

    # Reclamações Atendidas x Não Atendidas
    reclamacoes_rana = reclamacoes.values('atendida').annotate(num_reclamacoes=Count('atendida')).order_by(
        "-num_reclamacoes")
    qtd_reclamacoes = list()
    for r in reclamacoes_rana:
        qtd_reclamacoes.append(
            {
                "name": "Atendida" if r["atendida"] else "Não Atendida",
                "data": r["num_reclamacoes"],
            }
        )
    context["conjuntos_rana"] = qtd_reclamacoes
    context["titulo_grafico_rana"] = "Reclamações Atendidas x Não Atendidas"
    context["labely_rana"] = "Reclamações"

    # Fornecedores menos atenderam
    columns = ["CNPJ", "Razão Social", "Quantidade Reclamações Atendidas"]
    reclamacoes_fmaisa = reclamacoes.values('empresa', "empresa__cnpj", "empresa__razao_social_sindec",
                                            'atendida').filter(atendida=True).annotate(
        num_reclamacao=Count('atendida')).order_by("-num_reclamacao")
    qtd_reclamacoes = list()
    for fmaisa in reclamacoes_fmaisa[:100]:
        qtd_reclamacoes.append(
            {
                "name": fmaisa.get("empresa__cnpj"),
                "data": [fmaisa.get("empresa__razao_social_sindec"), fmaisa.get("num_reclamacao")],
            }
        )
    context["colunas_fmaisa"] = columns
    context["data_row_fmaisa"] = qtd_reclamacoes

    # Fornecedores mais atenderam
    columns = ["CNPJ", "Razão Social", "Quantidade Reclamações Não Atendidas"]
    qtd_reclamacoes = list()
    reclamacoes_fmenosa = reclamacoes.values('empresa', "empresa__cnpj", "empresa__razao_social_sindec",
                                             'atendida').filter(atendida=False).annotate(
        num_reclamacao=Count('atendida')).order_by("-num_reclamacao")
    for fmenosa in reclamacoes_fmenosa[:100]:
        qtd_reclamacoes.append(
            {
                "name": fmenosa.get("empresa__cnpj"),
                "data": [fmenosa.get("empresa__razao_social_sindec"), fmenosa.get("num_reclamacao")],
            }
        )
    context["colunas_fmenosa"] = columns
    context["data_row_fmenosa"] = qtd_reclamacoes

    # Fornecedores mais reclamados
    reclamacoes_fmr = reclamacoes.values("empresa__cnpj", "empresa__razao_social_sindec", ).annotate(
        num_reclamacao=Count('atendida')).order_by("-num_reclamacao")[:100]
    columns = ["CNPJ", "Razão Social", "Reclamações Atendidas", "%", "Reclamações Não Atendidas", "%",
               "Total de Reclamações", "%"]
    qtd_reclamacoes = list()
    for fmr in reclamacoes_fmr:
        atendida = reclamacoes.filter(empresa__cnpj=int(fmr.get("empresa__cnpj"))).filter(
            atendida=True).annotate(num_reclamacao=Count('atendida')).count()

        naoatendida = reclamacoes.filter(empresa__cnpj=fmr.get("empresa__cnpj")).filter(
            atendida=False).annotate(num_reclamacao=Count('atendida')).count()
        total = fmr.get("num_reclamacao")
        qtd_reclamacoes.append(
            {
                "name": fmr.get("empresa__cnpj"),
                "data": [
                    fmr.get("empresa__razao_social_sindec"),
                    atendida, ((atendida / total) * 100),
                    naoatendida, ((naoatendida / total) * 100),
                    total, (((total / len(reclamacoes)) * 100)),
                ],
            }
        )
    context["colunas_fmr"] = columns
    context["data_row_fmr"] = qtd_reclamacoes

    return context
