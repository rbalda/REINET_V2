__author__ = 'marlon'
from django import forms
from django.forms import PasswordInput, EmailInput
from django.contrib.auth.models import User
from usuarios.models import Perfil, Country

class RegistroUsuarioForm(forms.Form):
    username = forms.CharField(label="Usuario :", widget=forms.TextInput())
    password = forms.CharField(label="Password :", widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(label="Confirmar password :", widget=forms.PasswordInput(render_value=False))
    nombre = forms.CharField(label="Nombre :", widget=forms.TextInput())
    apellido = forms.CharField(label="Apellido :", widget=forms.TextInput())
    cedula = forms.CharField(label="Cedula :", widget=forms.TextInput())

    pais = forms.ModelChoiceField(queryset=Country.objects.all(),label="Pais :",initial=0)
    telefono = forms.CharField(label="Telefono :",widget=forms.TextInput)
    email = forms.EmailField(label="E-mail :", widget=forms.EmailInput())
    website = forms.URLField(max_length=20)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            u = User.objects.get(username=username)
        except u is None:
            return username
        raise forms.ValidationError('***Usuario ya existe***')
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            u = User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('***Correo ya registrado***')
    def clean_password2(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password==password2:
            pass
        else:
            raise forms.ValidationError('***Passwords no coinciden**')

