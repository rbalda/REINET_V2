# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Institucion',
            fields=[
                ('idinstitucion', models.AutoField(serialize=False, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=45)),
                ('siglas', models.CharField(max_length=12)),
                ('logo', models.TextField()),
                ('descripcion', models.CharField(max_length=500)),
                ('mision', models.CharField(max_length=500)),
                ('ubicacion', models.CharField(max_length=45)),
                ('web', models.CharField(max_length=45)),
                ('recursosofrecidos', models.CharField(max_length=200, null=True, blank=True)),
            ],
            options={
                'db_table': 'Institucion',
            },
        ),
        migrations.CreateModel(
            name='Membresia',
            fields=[
                ('idmembresia', models.AutoField(serialize=False, primary_key=True)),
                ('esadministrator', models.IntegerField()),
                ('cargo', models.CharField(max_length=45)),
                ('descripcion', models.CharField(max_length=45)),
                ('fecha', models.CharField(max_length=45)),
                ('ippeticion', models.CharField(max_length=45)),
                ('estado', models.IntegerField(null=True, blank=True)),
                ('fkinstitucion', models.ForeignKey(to='usuarios.Institucion')),
            ],
            options={
                'db_table': 'Membresia',
            },
        ),
        migrations.CreateModel(
            name='Mensaje',
            fields=[
                ('idmensaje', models.AutoField(serialize=False, primary_key=True)),
                ('mensaje', models.CharField(max_length=1000)),
                ('fecha', models.DateTimeField()),
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
                ('idperfil', models.AutoField(serialize=False, primary_key=True)),
                ('cedula', models.CharField(unique=True, max_length=10)),
                ('foto', models.TextField()),
                ('web', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=16)),
                ('fecharegistro', models.DateTimeField()),
                ('ipregistro', models.CharField(max_length=15)),
                ('reputacion', models.DecimalField(max_digits=4, decimal_places=0)),
                ('estado', models.IntegerField()),
                ('privacidad', models.CharField(max_length=11)),
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
                ('idpeticion', models.AutoField(serialize=False, primary_key=True)),
                ('nombre', models.CharField(max_length=45)),
                ('codigo', models.CharField(max_length=128)),
                ('usado', models.IntegerField()),
                ('fkusuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Peticion',
            },
        ),
        migrations.CreateModel(
            name='Ubicacion',
            fields=[
                ('idubicacion', models.AutoField(serialize=False, primary_key=True)),
                ('pais', models.CharField(max_length=45)),
                ('ciudad', models.CharField(max_length=45)),
                ('abreviatura', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'Ubicacion',
            },
        ),
        migrations.AddField(
            model_name='perfil',
            name='fkubicacion',
            field=models.ForeignKey(to='usuarios.Ubicacion'),
        ),
        migrations.AddField(
            model_name='mensaje',
            name='fkemisor',
            field=models.ForeignKey(related_name='fkemisor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='mensaje',
            name='fkreceptor',
            field=models.ForeignKey(related_name='fkreceptor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='membresia',
            name='fkusuario',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
