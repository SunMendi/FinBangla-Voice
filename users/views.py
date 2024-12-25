from django.shortcuts import render, redirect
from .models import Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm 
from django.db.models import Q
import json

# Create your views here.

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            #Do some shopping cart stuff
            current_user = Profile.objects.get(user__id=request.user.id)
           
            messages.success(request, ("You are now Logged in..."))
            return redirect('home')
        else:
            messages.warning(request, ("Error Logging In - Please try again !!!"))
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, "You are now logged out !!!")
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You Have Registered Successfully !!!")
            messages.success(request, "Please Update Your Profile Informations for Further Purposes.")
            return redirect('update_info')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
            return redirect('register')
    else:
        return render(request, 'register.html', {'form': form})
    
def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)
        
        if user_form.is_valid():
            user_form.save()
            
            login(request, current_user)
            messages.success(request, "Your profile has been updated successfully !!!")
            return redirect('home')
        return render(request, 'update_user.html', {'user_form': user_form})
    else:
        messages.success(request, "You must be logged in to view that page !!!")
        return redirect('home')
    
def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        #Did they fill out the form
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been updated successfully !!! Please Log in again.")
                # login(request, current_user)
                return redirect('login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                return redirect('update_password')

        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {'form':form})
    else:
        messages.success(request, "You must be logged in to view that page !!!")
        return redirect('home')
   
def update_info(request):
    if request.user.is_authenticated:
        #Get Current User
        current_user = Profile.objects.get(user__id=request.user.id)
    
        #Get Original User Form
        form = UserInfoForm(request.POST or None, instance=current_user)
        
        if form.is_valid():
            #Save original Form
            form.save()
            messages.success(request, "Your Profile Info has been Updated Successfully !!!")
            return redirect('home')
        return render(request, 'update_info.html', {'form': form})
    else:
        messages.success(request, "You must be logged in to view that page !!!")
        return redirect('home')