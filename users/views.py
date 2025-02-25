from django.shortcuts import render, redirect
from .models import Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .forms import SignUpForm
import json
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Profile  # Make sure this import is correct


def login_user(request):
    # If user is already authenticated, redirect to home
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You are now logged in.")
            return redirect("home")  # Redirect to home page after successful login
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, "login.html")

    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def logout_user(request):
    logout(request)
    messages.success(request, "You are now logged out!")
    return redirect("login")  # Redirect to login


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            # Log in user
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You have registered successfully!")
                messages.info(
                    request,
                    "Please update your profile information for further purposes.",
                )
                return redirect("update_info")
            else:
                messages.error(
                    request, "An error occurred during registration. Please try again."
                )
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = SignUpForm()
    return render(request, "register.html", {"form": form})


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, "Your profile has been updated successfully !!!")
            return redirect("home")
        return render(request, "update_user.html", {"user_form": user_form})
    else:
        messages.success(request, "You must be logged in to view that page !!!")
        return redirect("home")


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        # Did they fill out the form
        if request.method == "POST":
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(
                    request,
                    "Your password has been updated successfully !!! Please Log in again.",
                )
                # login(request, current_user)
                return redirect("login")
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                return redirect("update_password")

        else:
            form = ChangePasswordForm(current_user)
            return render(request, "update_password.html", {"form": form})
    else:
        messages.success(request, "You must be logged in to view that page !!!")
        return redirect("home")


def update_info(request):
    if request.user.is_authenticated:
        # Get Current User
        current_user = Profile.objects.get(user__id=request.user.id)

        # Get Original User Form
        form = UserInfoForm(request.POST or None, instance=current_user)

        if form.is_valid():
            # Save original Form
            form.save()
            messages.success(
                request, "Your Profile Info has been Updated Successfully !!!"
            )
            return redirect("home")
        return render(request, "update_info.html", {"form": form})
    else:
        messages.success(request, "You must be logged in to view that page !!!")
        return redirect("home")
