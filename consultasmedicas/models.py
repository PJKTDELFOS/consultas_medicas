from django.db import models
from mirage.fields import EncryptedCharField,EncryptedEmailField
from utilidades.utilitarios import valida_cpf



# Create your models here.


class Medico(models.Model):
    nomesocial=models.CharField(max_length=120)
    cpf=EncryptedCharField(max_length=11,validators=[valida_cpf],null=False,
                         blank=False,unique=True,
                         help_text="Insira um CPF válido (apenas números ou com pontuação")
    email=EncryptedEmailField(max_length=254,null=False,blank=False)

    profissao=models.CharField(max_length=120,null=False,blank=False)
    criado_em=models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = "Medico"
        verbose_name_plural = "Medicos"

    def __str__(self):
        return f'{self.nomesocial}:{self.profissao}'


class Consulta(models.Model):
    STATUS_CHOICES = [
        ('AGENDADA', 'Agendada'),
        ('CANCELADA', 'Cancelada'),
        ('REALIZADA', 'Realizada'),
    ]
    profissional=models.ForeignKey(Medico,on_delete=models.CASCADE,null=False,blank=False,related_name='consultas')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='AGENDADA')
    observacoes = models.TextField(blank=True, null=True)
    data_hora=models.DateTimeField()

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Consulta"
        verbose_name_plural = "Consultas"
        unique_together = ('profissional', 'data_hora')

    def __str__(self):
        # type: () -> str
        return f"Consulta com {self.profissional.nomesocial} em {self.data_hora.strftime('%d/%m/%Y %H:%M')}"





