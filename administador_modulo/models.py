from django.db import models
import datetime

# Create your models here.
from usuarios.models import Perfil, Institucion
from django.db import models
from django.contrib.auth.models import User
from cities_light.models import City, Country

class Administrador(User):
    id_administrador = models.AutoField(primary_key=True)


    
    class Meta:
        db_table = 'Administrador'

