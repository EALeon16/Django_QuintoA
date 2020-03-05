from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse

def cerrar(request):
    logout(request)
    return  HttpResponseRedirect(reverse('cliente'))

