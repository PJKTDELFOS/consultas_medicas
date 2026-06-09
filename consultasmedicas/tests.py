from datetime import timedelta
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from consultasmedicas.models import Medico, Consulta


class ClinicaCompletaAPITestCase(APITestCase):

    def setUp(self):
        """
        Prepara o terreno antes de CADA teste individual.
        """
        self.client = APIClient()
        self.usuario_teste = User.objects.create_user(
            username='tester_developer',
            email='teste@teste.com.br',
            password='teste@123456'
        )
        self.client.force_authenticate(user=self.usuario_teste)

        # Mapeamento das URLs conforme configurado no teu DefaultRouter (api_config/urls.py)
        # O teu router usa 'profissionais' e 'consulta'
        self.url_medicos = '/api/profissionais/'
        self.url_consultas = '/api/consulta/'

        # Criamos um médico base no banco temporário necessário para os testes de consulta
        self.medico_base = Medico.objects.create(
            nomesocial="Doutor Alfredo Reis",
            cpf="12345678909",  # Use um CPF que passe no teu valida_cpf
            email="alfredo@lacrei.com",
            profissao="Cardiologista"
        )

    def test_crud_medico_completo(self):
        """
        Testa o ciclo de vida feliz do Médico: Criar, Listar, Atualizar e Deletar.
        """
        # 1. CREATE (POST)
        dados_novos = {
            "nomesocial": "Doutora Amanda de Souza",
            "cpf": "98765432100",
            "email": "amanda@lacreisaude.com.br",
            "profissao": "Psicóloga"
        }
        response_create = self.client.post(self.url_medicos, dados_novos, format='json')
        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)
        medico_id = response_create.data['id']

        # 2. READ (GET list e GET detail)
        response_list = self.client.get(self.url_medicos, format='json')
        self.assertEqual(response_list.status_code, status.HTTP_200_OK)

        response_detail = self.client.get(f"{self.url_medicos}{medico_id}/", format='json')
        self.assertEqual(response_detail.status_code, status.HTTP_200_OK)
        self.assertEqual(response_detail.data['nomesocial'], "Doutora Amanda de Souza")

        # 3. UPDATE (PUT)
        dados_atualizados = {
            "nomesocial": "Doutora Amanda de Souza Santos",
            "cpf": "98765432100",
            "email": "amanda.santos@lacreisaude.com.br",
            "profissao": "Neuropsicóloga"
        }
        response_update = self.client.put(f"{self.url_medicos}{medico_id}/", dados_atualizados, format='json')
        self.assertEqual(response_update.status_code, status.HTTP_200_OK)
        self.assertEqual(Medico.objects.get(id=medico_id).profissao, "Neuropsicóloga")

        # 4. DELETE (DELETE)
        response_delete = self.client.delete(f"{self.url_medicos}{medico_id}/")
        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)

    def test_cadastro_medico_cpf_invalido(self):
        """
        Regra de Erro: Garante que a API bloqueia CPFs falsos/inválidos (HTTP 400).
        """
        dados_invalidos = {
            "nomesocial": "Doutor Carlos",
            "cpf": "11111111111",
            "email": "carlos@lacrei.com",
            "profissao": "Psiquiatra"
        }
        response = self.client.post(self.url_medicos, dados_invalidos, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_crud_consulta_completo(self):
        """
        Testa o ciclo de vida feliz da Consulta: Criar, Listar, Atualizar e Deletar.
        """
        # 1. CREATE (POST)
        data_futura = timezone.now() + timedelta(days=2)
        dados_consulta = {
            "profissional": self.medico_base.id,
            "data_hora": data_futura,
            "status": "AGENDADA",
            "observacoes": "Primeira consulta de rotina."
        }
        response_create = self.client.post(self.url_consultas, dados_consulta, format='json')
        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)
        consulta_id = response_create.data['id']

        # 2. READ (GET list e busca por ID do profissional na URL)
        response_list = self.client.get(self.url_consultas, format='json')
        self.assertEqual(response_list.status_code, status.HTTP_200_OK)

        response_filter = self.client.get(f"{self.url_consultas}?profissional={self.medico_base.id}", format='json')
        self.assertEqual(response_filter.status_code, status.HTTP_200_OK)

        # 3. UPDATE (PATCH)
        dados_patch = {"status": "REALIZADA"}
        response_patch = self.client.patch(f"{self.url_consultas}{consulta_id}/", dados_patch, format='json')
        self.assertEqual(response_patch.status_code, status.HTTP_200_OK)
        self.assertEqual(Consulta.objects.get(id=consulta_id).status, "REALIZADA")

        # 4. DELETE (DELETE)
        response_delete = self.client.delete(f"{self.url_consultas}{consulta_id}/")
        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)

    def test_agenda_consulta_no_passado_bloqueado(self):
        """
        Regra de Erro: Impede agendamentos retroativos (HTTP 400).
        """
        data_passada = timezone.now() - timedelta(days=1)
        dados_invalidos = {
            "profissional": self.medico_base.id,
            "data_hora": data_passada,
            "status": "AGENDADA"
        }
        response = self.client.post(self.url_consultas, dados_invalidos, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_choque_de_horario_no_mesmo_medico(self):
        """
        Regra de Erro: unique_together impede o mesmo médico ter duas consultas no mesmo horário.
        """
        horario_comum = timezone.now() + timedelta(days=5)

        # Primeira consulta criada direto no banco
        Consulta.objects.create(profissional=self.medico_base, data_hora=horario_comum)

        # Tentativa de mandar o POST para a API no mesmíssimo horário
        dados_duplicados = {
            "profissional": self.medico_base.id,
            "data_hora": horario_comum,
            "status": "AGENDADA"
        }
        response = self.client.post(self.url_consultas, dados_duplicados, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)