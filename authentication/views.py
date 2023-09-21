from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

# Create your views here.
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/CMA')
    else:
        form = AuthenticationForm(request)
    context = {"form":form}
    return render(request, "authentication/login.html", context)

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("/auth/login")
    return render(request, "authentication/logout.html")

def register_view(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user_obj = form.save()
        return redirect('/auth/login')
    context = {"form": form}
    return render(request, "authentication/register.html", context)
