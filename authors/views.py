from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from .login_register_forms import LoginForm, RegisterForm


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


@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        messages.error(request, 'Invalid logout request')
        return redirect(reverse('authors:login'))
    if request.POST.get('username') != request.user.username:
        messages.error(request, 'Invalid user')
        return redirect(reverse('authors:login'))

    messages.success(request, 'You are now logged out')
    logout(request)
    return redirect(reverse('authors:login'))
