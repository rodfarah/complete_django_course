from django.http.response import Http404
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.db.models import Q
from recipes.models import Recipe
# from utils.recipes.factory import make_recipe


def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    return render(
        request=request, template_name='recipes/pages/home.html',
        context={'recipes': recipes})


def category(request, category_id):
    recipes = get_list_or_404(klass=Recipe.objects.filter(
        category__id=category_id, is_published=True,).order_by('-id'))

    return render(
        request, 'recipes/pages/category.html',
        context={
            'recipes': recipes,
            'category_name': f'{recipes[0].category.name} - Category | '
        }
    )


def recipe(request, id):
    recipe = get_object_or_404(klass=Recipe, pk=id, is_published=True,)
    return render(
        request, 'recipes/pages/recipe-view.html',
        context={
            'recipe': recipe,
            'is_detail_page': True
        })


def search(request):
    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()

    recipes = Recipe.objects.filter(
        # __contains is a django resource. The query text is PART of the search
        # __icontains is the same, but django also ignores Caps.
        # Q is the same as 'OR' in a db query.
        # | (pipe) is also the same as 'OR' in a db query.
        # result must be published
        Q(title__icontains=search_term) |
        Q(description__icontains=search_term),
        is_published=True
    ).order_by('-id')
    return render(
        request,
        'recipes/pages/search.html',
        context={
            'page_title': f'Search for "{search_term}" |',
            'search_term': search_term,
            'recipes': recipes
        }
    )
