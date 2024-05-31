from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.http import Http404
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login


def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    return render(request, 'authors/pages/register_view.html', {
        'form': form,
        'form_action': reverse("authors:register_create")
    })


def register_create(request):
    if not request.POST:
        raise Http404
    else:
        POST = request.POST
        request.session['register_form_data'] = POST
        form = RegisterForm(POST)

        if form.is_valid():
            user = form.save(commit=False)
            # encript password
            user.set_password(user.password)
            user.save()
            messages.success(request, 'You are now registered! Please, Log In')
            del (request.session['register_form_data'])
    return redirect(to='authors:register')


def login_view(request):
    form = LoginForm()
    return render(
        request, 'authors/pages/login.html',
        context={'form': form, 'form_action': reverse('authors:login_create')})


def login_create(request):
    if not request.POST:
        raise Http404()

    form = LoginForm(request.POST)
    login_url = reverse('authors:login')
    if form.is_valid():
        username = form.cleaned_data.get('username', '')
        password = form.cleaned_data.get('password', '')
        authenticated_user = authenticate(
            username=username,
            password=password)
        if authenticated_user is not None:
            messages.success(
                request, f'You are now logged in as {username}!')
            login(request, authenticated_user)
        else:
            messages.error(
                request,
                'Invalid username and/or password. Please, try again.')
    else:
        messages.error(
            request, 'Form data is not valid.')
    return redirect(login_url)
