from django.shortcuts import render


def home(request):
    return render(
        request=request, template_name="recipes/home.html",
        context={"name": "Rodrigo Farah"})
