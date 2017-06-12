from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User




class Projeto(models.Model):
    nome = models.CharField('nome', max_length=100)

    def __str__(self):
        return '{}'.format(self.nome)



class ProjetoUsuario(models.Model):
    projeto = models.ForeignKey('Projeto')
    usuario = models.OneToOneField(User)



class Tarefa(models.Model):
    nome = models.CharField('nome', max_length=100)
    dataEHoraDeInicio = models.DateTimeField('dataEHoraDeInicio', default=timezone.now)
    usuario = models.ForeignKey(User)
    projeto = models.ForeignKey('Projeto')