from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(
        request=request, template_name="recipes/home.html",
        context={"name": "Rodrigo Farah"})


def contact(request):
    return render(request=request, template_name="recipes/contact.html")


def about(request):
    return HttpResponse("ABOUT")
