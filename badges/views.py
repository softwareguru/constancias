from django.shortcuts import render

from django.http import HttpResponse


def index(request):
    return HttpResponse("<h1>Hola</h1><p>En algún lugar por aquí está tu constancia, pero necesitas el url.</p>")