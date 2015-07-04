from django.test import TestCase
from django.test import Client
from models import *
# Create your tests here.
class registroTest(TestCase):



	def test_registrarEmailRepetido(self):
		self.crear_usuario(self.form1())
		user2=self.form2()
		status=self.crear_usuario( self.form2())
		#self.assertTrue(Perfil.objects.filter(username=username_esperado).exists(), True)
		username_esperado=user2['username']
		self.assertTrue(Perfil.objects.filter(username=username_esperado).exists(), True)


	def form1(self):
		return { 'username':'usuario111',
		'nombres':'Angel',
		'apellidos':'Guale',
		'password1':'123',
		'cedula':'0101010111',
		'telefono':'0909090909',
		'website':'http://hola.com',
		'email':'angel1@guale.com',
		'pais':'2',
		'ciudad':'2',
		}	
	def form2(self):
			return { 'username':'usuario222',
			'nombres':'Angel',
			'apellidos':'Guale',
			'password1':'123',
			'cedula':'0101010122',
			'telefono':'0909090909',
			'website':'http://hola.com',
			'email':'angel1@guale.com',
			'pais':'2',
			'ciudad':'2',
			}	
	def crear_usuario(self, form):
		c=Client()
		response = c.post('/registro_usuario/', form)
		print response.status_code
		return response.status_code