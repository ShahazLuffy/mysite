from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Tutorial, TutorialSeries, TutorialCategory
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import NewUserForm


def homepage(request):
    return render(request=request,
                  template_name="main/categories.html",
                  context={"categories": TutorialCategory.objects.all})


def register(request):
    if request.method == 'POST':
        form = NewUserForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"new account created: {username}")
            login(request, user)
            messages.info(request, f"you are now logged in as  {username}")
            return redirect('main:homepage')
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}:{form.error_messages[msg]}")

    form = NewUserForm
    return render(request,
                  'main/register.html', context={
            'form': form})


def logout_request(request):
    logout(request)
    messages.info(request, "logged out successfully!")
    return redirect("main:homepage")


def login_reuqest(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"you are now logged in as  {username}")
                return redirect("main:homepage")
            else:
                messages.warning(request, "invalid username or password")

    else:
        messages.warning(request, "invalid username or password")
    form = AuthenticationForm()
    return render(request, 'main/login.html',
                  {"form": form})


def single_slug(request, single_slug):
    categories = [c.category_slug for c in TutorialCategory.objects.all()]
    if single_slug in categories:
        return HttpResponse(f"{single_slug} is a Category")

    tutorials = [t.tutorial_slug for t in Tutorial.objects.all()]
    if single_slug in tutorials:
        return HttpResponse(f"{single_slug} is a Tutorial")
    return HttpResponse(f"{single_slug} does not corresponds to anything")
