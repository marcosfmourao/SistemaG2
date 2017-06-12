from tastypie.resources import ModelResource
from tastypie import fields
from cad.models import *
from django.contrib.auth.models import User
from tastypie.authorization import Authorization
from tastypie.authentication import BasicAuthentication, ApiKeyAuthentication
from tastypie.exceptions import Unauthorized



class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['password', 'is_active']

    def obj_delete_list(self, bundle, **kwargs):
        raise Unauthorized("Não é possível apagar a lista!")




class ProjetoResource(ModelResource):

    def obj_create(self, bundle, **kwargs):
        if not (Projeto.objects.filter(nome=bundle.data['nome'])):
            projeto = Projeto()
            projeto.nome = bundle.data['nome']
            projeto.save()
            bundle.obj = projeto
            return bundle
        else:
            raise Unauthorized('Já existe um projeto com este nome')

    def obj_delete_list(self, bundle, **kwargs):
        raise Unauthorized("Não é possível apagar a lista!")

    class Meta:
        queryset = Projeto.objects.all()
        allowed_methods = ['get', 'post', 'delete', 'put']
        authorization = Authorization()
        #authentication = ApiKeyAuthentication()
        filtering = {
            "nome": ('exact', 'startswith',)
        }

class ProjetoUsuarioResource(ModelResource):
    def obj_delete_list(self, bundle, **kwargs):
        raise Unauthorized("Não é possivel deletar toda a lista!")

    usuario = fields.ToOneField(UserResource, 'usuario')
    projeto = fields.ToOneField(ProjetoResource, 'projeto')
    class Meta:
        queryset = ProjetoUsuario.objects.all()
        allowed_methods = ['get', 'post', 'delete', 'put']
        authorization = Authorization()
        filtering = {
            "descricao": ('exact', 'startswith')
        }


class TarefaResource(ModelResource):
    usuario = fields.ToOneField(UserResource, 'usuario')
    projeto = fields.ToOneField(ProjetoResource, 'projeto')

    class Meta:
        queryset = Tarefa.objects.all()
        allowed_methods = ['get', 'post', 'delete', 'put']
        authorization = Authorization()
        filtering = {
            "titulo": ('exact', 'startswith',)
        }

    def obj_create(self, bundle, **kwargs):
        u = bundle.data['usuario'].split("/")[-2]
        p = bundle.data['projeto'].split("/")[-2]

        if not Tarefa.objects.filter(nome=bundle.data['nome']):
            tarefa = Tarefa()
            tarefa.nome = bundle.data['nome']
            tarefa.dataEHoraDeInicio = bundle.data['dataEHoraDeInicio']
            tarefa.usuario = User.objects.get(pk=u)
            tarefa.projeto = Projeto.objects.get(pk=p)
            tarefa.save()
            bundle.obj = tarefa
            return bundle
        else:
            raise Unauthorized("Tarefa ja cadastrada.")

    def obj_delete_list(self, bundle, **kwargs):
        raise Unauthorized("Não é possível apagar a lista!")