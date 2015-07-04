from django.contrib import admin

# Register your models here.
from usuarios.models import Peticion, Mensaje,Notificacion

admin.site.register(Peticion)
admin.site.register(Mensaje)
admin.site.register(Notificacion)