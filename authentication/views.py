from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from authentication.forms import UserCreateForm, AuthenticateForm

def login_view(request):
    if request.method == "POST":
        form = AuthenticateForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get("next")
            if next_url is None:
                next_url = "/"    
            return redirect(next_url)
        else:
            # Add an error message if authentication fails
            messages.ERROR(request, 'Invalid username or password')
    else:
        form = AuthenticateForm(request)
    context = {"form":form}
    return render(request, "auth/login.html", context)

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("/")
    return render(request, "auth/logout.html")

def register_view(request):
    if request.method == "POST":
        form = UserCreateForm(request.POST or None)
        if form.is_valid():
            user_obj = form.save()
            return redirect('/auth/login')
        else:
            # Add an error message if registration fails
            messages.ERROR(request, 'Invalid registration details')
    else:
        form = UserCreateForm()
    context = {"form": form}
    return render(request, "auth/register.html", context)
