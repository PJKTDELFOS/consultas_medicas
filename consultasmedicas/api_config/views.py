from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import viewsets

from consultasmedicas.api_config.serializers import MedicoSerializer, ConsultaSerializer
from consultasmedicas.models import Consulta,Medico


class ViewMedicos(viewsets.ModelViewSet):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer
    permission_classes = [IsAuthenticated,]




class ViewConsulta(viewsets.ModelViewSet):
    queryset = Consulta.objects.all()
    serializer_class = ConsultaSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        lista_completa=super().get_queryset()
        profissional_id=self.request.query_params.get('profissional')

        if profissional_id and profissional_id.strip():
            return lista_completa.filter(profissional_id=profissional_id.strip())
        return lista_completa



