from rest_framework import serializers
from django.utils import timezone
from consultasmedicas import models


class MedicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Medico
        fields = '__all__'
        read_only_fields = 'id','criado_em'
    def validate_nomesocial(self, data):

        if not data or not data.strip():
            raise serializers.ValidationError(' o nome social  nao pode esta vazio')
        return data.strip()
    def validate_profissao(self, data):
        if not data or not data.strip():
            raise serializers.ValidationError(' o profissao nao pode esta vazio')
        return data.strip()

class ConsultaSerializer(serializers.ModelSerializer):
    profissional_detalhes=MedicoSerializer(source='profissional',read_only=True)
    class Meta:
        model = models.Consulta
        fields = '__all__'
        read_only_fields = 'id','criado_em','atualizado_em'

    def validate_data_hora(self, data):
        if  data < timezone.now():
            raise serializers.ValidationError('Não é possível agendar uma consulta numa data ou hora passada')
        return data