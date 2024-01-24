from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from authentication.forms import UserCreateForm, AuthenticateForm, ProfileForm, CustomPasswordChangeForm, SettingsForm
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
            if form.cleaned_data['ToS']:
                user_obj = form.save()
                messages.success(request, 'Account created successfully')
                return redirect('/auth/login')
            else:
                messages.error(request, 'Please agree to the Terms of Service.')
        else:
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

def settings_view(request):
    user = request.user
    if request.method == "POST":
        settings_form = SettingsForm(request.POST or None)
        if settings_form.is_valid():
            user.settings = {
                'font_size': settings_form.cleaned_data['font_size'],
                'chunk_size': settings_form.cleaned_data['chunk_size'],
                'sentence_cut_percentage': settings_form.cleaned_data['sentence_cut_percentage'],
                'modelChoice': settings_form.cleaned_data['modelChoice']
            }
            user.save()
            messages.success(request, 'Your settings were successfully updated!')
            return redirect('/auth/settings')
        else:
            messages.error(request, 'Update failed')
            return redirect('/auth/settings')
    else:
        initial_data = {
            'font_size': user.settings.get('font_size', 16) if user.settings else 16,
            'chunk_size': user.settings.get('chunk_size', 1000) if user.settings else 1000,
            'sentence_cut_percentage': user.settings.get('sentence_cut_percentage', 25.0) if user.settings else 25.0,
            'modelChoice': user.settings.get('modelChoice', 'roberta-base-squad2') if user.settings else 'roberta-base-squad2',
        }
        settings_form = SettingsForm(initial=initial_data)

    context = {"settings_form": settings_form, "user": request.user}
    return render(request, "auth/settings.html", context)
