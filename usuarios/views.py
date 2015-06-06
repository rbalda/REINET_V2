# -*- encoding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template.context_processors import csrf
from models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

def registro_institucion(request):

    return render_to_response('Institucion_Sign-up.html',{})




def index(request):

    return render_to_response('index.html',{})