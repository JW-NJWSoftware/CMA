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
            next_url = request.GET.get("next")    
            return redirect(next_url)
    else:
        form = AuthenticationForm(request)
    context = {"form":form}
    return render(request, "auth/login.html", context)

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("/")
    return render(request, "auth/logout.html")

def register_view(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user_obj = form.save()
        return redirect('/auth/login')
    context = {"form": form}
    return render(request, "auth/register.html", context)
