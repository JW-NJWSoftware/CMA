from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from authentication.forms import UserCreateForm, AuthenticateForm, ProfileForm, CustomPasswordChangeForm
from authentication.models import CustomUser

def login_view(request):
    if request.method == "POST":
        form = AuthenticateForm(request, data=request.POST)
        if form.is_valid():

            user = form.get_user()
            login(request, user)
            user.save()

            next_url = request.GET.get("next")
            if next_url is None:
                next_url = "/"    
            return redirect(next_url)
        else:
            # Add an error message if authentication fails
            messages.error(request, 'Invalid username or password')
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
            messages.success(request, 'Account created successfully')
            return redirect('/auth/login')
        else:
            # Add an error message if registration fails
            messages.error(request, 'Invalid registration details')
    else:
        form = UserCreateForm()
    context = {"form": form}
    return render(request, "auth/register.html", context)

def profile_view(request):
    user = request.user
    if request.method == "POST":
        if "update_profile" in request.POST:
            profile_form = ProfileForm(request.POST or None, instance=request.user)
            if profile_form.is_valid():
                user_obj = profile_form.save()
                messages.success(request, 'Your account was successfully updated!')
                return redirect('/auth/profile')
            else:
                messages.error(request, 'Update failed')
                return redirect('/auth/profile')
        elif "change_password" in request.POST:
            password_form = CustomPasswordChangeForm(user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                return redirect('/auth/profile')

    else:
        profile_form = ProfileForm(instance=user)
        password_form = CustomPasswordChangeForm(user)

    context = {"profile_form": profile_form, "user": request.user, 'password_form': password_form}
    return render(request, "auth/profile.html", context)
