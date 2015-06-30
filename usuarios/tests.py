from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from django.test import Client
# Create your tests here.
class registroTest(TestCase):



	def test_registrarEmailRepetido(self):
		self.crear_usuario(self, self.form1(self))
		#username_esperado=self.form2(self)
		status=self.crear_usuario(self, self.form2(self))
		#self.assertTrue(Perfil.objects.filter(username=username_esperado).exists(), True)
	


	def form1(self):
		return { 'username':'usuario11',
		'nombres':'Angel',
		'apellidos':'Guale',
		'password1':'123',
		'cedula':'0101010101',
		'telefono':'0909090909',
		'website':'http://hola.com',
		'email':'angel@guale.com',
		'pais':'2',
		'ciudad':'2',
		}	
	def form2(self):
			return { 'username':'usuario22',
			'nombres':'Angel',
			'apellidos':'Guale',
			'password1':'123',
			'cedula':'0101010102',
			'telefono':'0909090909',
			'website':'http://hola.com',
			'email':'angel@guale.com',
			'pais':'2',
			'ciudad':'2',
			}	
	def crear_usuario(self, form):
		c=Client()
		response = c.post('/registro_usuario/', form)
		print response.status_code
		return response.status_code



