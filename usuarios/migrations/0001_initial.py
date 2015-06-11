# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.auth.models
import usuarios.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cities_light', '0004_auto_20150610_1323'),
    ]

    operations = [
        migrations.CreateModel(
            name='Institucion',
            fields=[
                ('id_institucion', models.AutoField(serialize=False, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=45)),
                ('siglas', models.CharField(max_length=12)),
                ('logo', models.ImageField(upload_to=b'')),
                ('descripcion', models.CharField(max_length=500)),
                ('mision', models.CharField(max_length=500)),
                ('web', models.CharField(max_length=45)),
                ('recursos_ofrecidos', models.CharField(max_length=200, null=True, blank=True)),
                ('correo', models.EmailField(default=None, max_length=254)),
                ('telefono_contacto', models.CharField(default=None, max_length=15)),
                ('ciudad', models.ForeignKey(related_name='ciudad_origen', default=None, to='cities_light.City')),
            ],
            options={
                'db_table': 'Institucion',
            },
        ),
        migrations.CreateModel(
            name='Membresia',
            fields=[
                ('id_membresia', models.AutoField(serialize=False, primary_key=True)),
                ('es_administrator', models.BooleanField(default=False)),
                ('cargo', models.CharField(max_length=45)),
                ('descripcion_cargo', models.CharField(max_length=45)),
                ('fecha_peticion', models.DateTimeField(auto_now_add=True)),
                ('fecha_aceptacion', models.DateTimeField(default=None)),
                ('ip_peticion', models.GenericIPAddressField()),
                ('estado', models.BooleanField(default=False)),
                ('fk_institucion', models.ForeignKey(to='usuarios.Institucion')),
            ],
            options={
                'db_table': 'Membresia',
            },
        ),
        migrations.CreateModel(
            name='Mensaje',
            fields=[
                ('id_mensaje', models.AutoField(serialize=False, primary_key=True)),
                ('mensaje', models.CharField(max_length=1000)),
                ('fecha_de_envio', models.DateTimeField()),
                ('asunto', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'Mensaje',
            },
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, to=settings.AUTH_USER_MODEL)),
                ('id_perfil', models.AutoField(serialize=False, primary_key=True)),
                ('cedula', models.CharField(unique=True, max_length=10)),
                ('foto', models.ImageField(default='noPicture.png', upload_to=usuarios.models.get_upload_path)),
                ('web', models.URLField()),
                ('telefono', models.CharField(max_length=16)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('ip_registro', models.GenericIPAddressField()),
                ('reputacion', models.DecimalField(default=0, max_digits=4, decimal_places=0)),
                ('estado', models.PositiveSmallIntegerField(default=1)),
                ('privacidad', models.BinaryField(max_length=8)),
                ('actividades', models.TextField()),
                ('fk_ciudad', models.ForeignKey(related_name='ciudad_de_origen', default=None, to='cities_light.City')),
                ('fk_pais', models.ForeignKey(related_name='pais_de_origen', default=None, to='cities_light.Country')),
            ],
            options={
                'db_table': 'Perfil',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Peticion',
            fields=[
                ('id_peticion', models.AutoField(serialize=False, primary_key=True)),
                ('nombre_institucion', models.CharField(max_length=45)),
                ('codigo', models.CharField(max_length=128)),
                ('usado', models.BooleanField(default=False)),
                ('fk_usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Peticion',
            },
        ),
        migrations.AddField(
            model_name='mensaje',
            name='fk_emisor',
            field=models.ForeignKey(related_name='mensajes_enviados', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='mensaje',
            name='fk_receptor',
            field=models.ForeignKey(related_name='mensajes_receptados', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='membresia',
            name='fk_usuario',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='institucion',
            name='miembros',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='usuarios.Membresia'),
        ),
        migrations.AddField(
            model_name='institucion',
            name='pais',
            field=models.ForeignKey(related_name='pais_origen', default=None, to='cities_light.Country'),
        ),
    ]
