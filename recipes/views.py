from django.shortcuts import render


def home(request):
    return render(
        request=request, template_name="recipes/pages/home.html",
        context={"name": "Rodrigo Farah"})


def recipe(request, id):
    return render(
        request=request, template_name="recipes/pages/recipe-view.html",
        context={"name": "Rodrigo Farah"})
