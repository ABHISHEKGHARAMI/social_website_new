from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate,login
from .forms import LoginForm , UserRegistrationForm , UserEditForm , ProfileEditForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile



# Create your views here.


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return HttpResponse('authenticated and login successfully')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(
        request,
        'account/login.html',
        {
            'form':form
        }
    )




# dashboard view
@login_required
def dashboard(request):
    return render(
        request,
        'account/dashboard.html',
        {
            'section':'dashboard'
        }
    )
    
#  register new user 
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            
            new_user = user_form.save(commit=False)
            
            # set the password
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            # save the user
            new_user.save()
            # create new user
            Profile.objects.create(user=new_user)
            messages.success(request,f"Welcome {new_user.username}")
            return render(
                request,
                'account/register_done.html',
                {
                    'new_user':new_user
                }
            )
        
    else:
        user_form = UserRegistrationForm()
        messages.error(request,"please try again!!")
        
    return render(
        request,
        'account/register.html',
        {
            'user_form':user_form
        }
    )
    
    
@login_required
def edit(request):
    if request.method == 'POST':
        user_form= UserEditForm(
            instance = request.user,
            data = request.POST
        )
        
        profile_form= ProfileEditForm(
            instance = request.user.profile,
            data = request.POST,
            files = request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            # profile create of the user
            
            messages.success(request,"Profile edited successfully")
        else:
            messages.error(request,"Profile can not update")
    else:
        user_form= UserEditForm(instance=request.user)
        profile_form= ProfileEditForm(instance=request.user.profile)
        
    return render(
        request,
        'account/edit.html',
        {
            'user_form':user_form,
            'profile_form':profile_form
        }
    )