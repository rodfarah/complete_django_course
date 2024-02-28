from django.shortcuts import render
from utils.recipes.factory import make_recipe


def home(request):
    return render(
        request=request, template_name="recipes/pages/home.html",
        context={"recipes": [make_recipe() for n in range(10)]})


def recipe(request, id):
    return render(
        request=request, template_name="recipes/pages/recipe-view.html",
        context={"receita": make_recipe()})
