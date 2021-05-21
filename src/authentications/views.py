from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm, UserLoginForm
from django.views.decorators.csrf import ensure_csrf_cookie

User = get_user_model()


# Create your views here.

def auth_view(req):
    if req.user.is_authenticated:
        return redirect('/')

    return redirect('auth/login')


def login_view(request):


    if request.user.is_authenticated:
        return redirect("/")
    next = request.GET.get('next')

    form = UserLoginForm(request.POST or None)

    if request.method == "POST":
        print(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            if next:
                return redirect(next)

            return redirect("/")

    context = {
        "form": form
    }
    return render(request, 'auth/login.html', context)


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()

    context = {
        'form': form
    }
    return render(request, "auth/signup.html", context)


def logout_view(request):
    if not request.user.is_authenticated:
        return redirect("/")

    logout(request)
    return redirect("/")


def password_change_view(req):
    pass


def forgot_password_view(req):
    pass


def delete_account_view(req):
    pass


def change_email_view(req):
    pass
