# encoding: utf-8

from django.conf import settings
from django.http import HttpResponse
import csv
from os.path import join as join_path
from sindec import models


def csv_test(request, *args, **kwargs):
#    files = ['reclamacoes-fundamentadas-sindec-2009-v2.csv', ]
#    files = ['reclamacoes-fundamentadas-sindec-2010-v2.csv', ]
    files = [
        'reclamacoes-fundamentadas-sindec-2011-v2.csv', 
        'reclamacoes-fundamentadas-sindec-2012-v2.csv',
        'reclamacoes-fundamentadas-sindec-2012-2-v2.csv',
        'reclamacoes-fundamentadas-sindec-2012-3-v2.csv',
        'reclamacoes-fundamentadas-sindec-2013-v2.csv', 
        'reclamacoes-fundamentadas-sindec-2014-v2.csv', 
        ]
    result = ""
    for file_name in files:
        csv_path = join_path(join_path(settings.BASE_DIR, "db_init"), file_name)
        try:
            with open(csv_path, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=";", quotechar='"')
                for row in reader:
                    print("Lendo linha...")
                    if reader.line_num != 1:
                        try:
                            # print(row)
                            result += "<br/><h1>LINE: {}</h1><br/>".format(reader.line_num)
                            # result += "CNAE lines:<br/>"

                            # Dicionário de dados de empresa
                            cnae_dict = dict()
                            cnae_dict[header[13]] = row[13]
                            cnae_dict[header[14]] = row[14]

                            # create cnae object
                            cnae_obj = models.CNAE(**cnae_dict)
                            # save cnae object
                            cnae_obj.save()

                            # result += cnae_dict.__str__()
                            # result += "<br/>"

                            # result += "Empresa lines:<br/>"
                            # Dicionario de dados de empresa
                            empresa_dict = dict()
                            empresa_dict[header[6]] = row[6]
                            empresa_dict[header[7]] = row[7]
                            empresa_dict[header[8]] = True if row[8] == '1' else False
                            empresa_dict[header[9]] = row[9]
                            empresa_dict[header[10]] = row[10]
                            empresa_dict[header[11]] = row[11]
                            empresa_dict[header[12]] = row[12]

                            # create empresa object
                            empresa_obj = models.Empresa(**empresa_dict)
                            # add cnae object
                            empresa_obj.cnae = cnae_obj
                            # save empresa
                            empresa_obj.save()

                            # result += empresa_dict.__str__()
                            # result += "<br/>"

                            # result += "Procom lines:<br/>"
                            procom_dict = dict()
                            procom_dict[header[3]] = row[3]
                            procom_dict[header[5]] = row[5]
                            procom_dict["username"] = "{}_{}".format(row[3], row[5])

                            # create procom object
                            procom_obj = models.Procom.objects.filter(username=procom_dict["username"])
                            if len(procom_obj) == 0:
                                procom_obj = models.Procom(**procom_dict)
                                procom_obj.password = "pbkdf2_sha256$20000$yRCSHq4uIPxb$IMZOYDnlRWvr+8vbTH1rCDbHPy32mKLEGcoM3P7fq4E="
                                procom_obj.is_staff = True
                                # save procom
                                procom_obj.save()
                            else:
                                procom_obj = procom_obj[0]

                            # result += procom_dict.__str__()
                            # result += "<br/>"

                            # result += "Consumidor lines:<br/>"
                            consumidor_dict = dict()
                            consumidor_dict[header[20]] = row[20]
                            for fe in models.Consumidor.CHOICES_FE:
                                if row[21] == fe[1]:
                                    consumidor_dict[header[21]] = fe[0]
                                    break
                            consumidor_dict[header[22]] = row[22]

                            # create consumidor object
                            consumidor_obj = models.Consumidor(**consumidor_dict)
                            # save consumidor
                            consumidor_obj.save()

                            # result += consumidor_dict.__str__()
                            # result += "<br/>"

                            # result += "Problema lines:<br/>"
                            problema_dict = dict()
                            problema_dict[header[18]] = row[18]
                            problema_dict[header[19]] = row[19]

                            # create problema object
                            problema_obj = models.Problema(**problema_dict)
                            # save problema
                            problema_obj.save()

                            # result += problema_dict.__str__()
                            # result += "<br/>"

                            # result += "Assunto lines:<br/>"
                            assunto_dict = dict()
                            assunto_dict[header[16]] = row[16]
                            assunto_dict[header[17]] = row[17]

                            # create assunto object
                            assunto_obj = models.Assunto(**assunto_dict)
                            # save assunto
                            assunto_obj.save()

                            # result += assunto_dict.__str__()
                            # result += "<br/>"

                            # result += "Reclamação lines:<br/>"
                            reclamacao_dict = dict()
                            reclamacao_dict[header[0]] = row[0]
                            reclamacao_dict[header[1]] = row[1]
                            reclamacao_dict[header[2]] = row[2]
                            reclamacao_dict[header[15]] = True if row[15] == "S" else False


                            # create reclamacao object
                            reclamacao_obj = models.Reclamacao(**reclamacao_dict)
                            reclamacao_obj.reclamador = consumidor_obj
                            reclamacao_obj.registrador = procom_obj
                            reclamacao_obj.empresa = empresa_obj
                            reclamacao_obj.assunto = assunto_obj
                            reclamacao_obj.problema = problema_obj

                            # save reclamacao
                            reclamacao_obj.save()

                            # result += reclamacao_dict.__str__()
                            # result += "<br/>"
                        except Exception as e:
                            print(e)
                            continue
                    else:
                        header = row
                    print("... linha lida!")

        except FileExistsError as e:
            print(e)
            result = HttpResponse("Erro em ler o arquivo!")
            csvfile.close()
        finally:
            csvfile.close()
    result = HttpResponse(result)
    return result
