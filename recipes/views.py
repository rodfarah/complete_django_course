from django.shortcuts import render, get_object_or_404, get_list_or_404
# from utils.recipes.factory import make_recipe
from .models import Recipe


def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    return render(
        request=request, template_name="recipes/pages/home.html",
        context={"recipes": recipes})


def category(request, category_id):
    recipes = get_list_or_404(klass=Recipe.objects.filter(
        category__id=category_id, is_published=True).order_by('-id'))

    return render(
        request, 'recipes/pages/category.html',
        context={
            "recipes": recipes,
            "category_name": f'{recipes[0].category.name} - Category |'
        }
    )


def one_recipe(request, one_id):
    one_recipe = get_object_or_404(klass=Recipe, id=one_id, is_published=True)
    return render(
        request, "recipes/pages/recipe-view.html",
        context={
            "recipes": one_recipe,
            "is_detail_page": True
        })
