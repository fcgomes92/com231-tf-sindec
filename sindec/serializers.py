from rest_framework import serializers
from sindec.models import Reclamacao

class ReclamacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reclamacao
        depth = 1