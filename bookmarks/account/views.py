from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponse
from .forms import LoginForm
# Create your views here.


# user login view
def user_login(request):
    # if request method is post then
    if request.method == "POST":
        # get the data from the login form
        form = LoginForm(request.POST)
        # check form is valid
        if form.is_valid():
            # if it is valid cleaned the data
            cd = form.cleaned_data
            # authenticate the user
            user = authenticate(
                request,
                username = cd['username'],
                password=cd['password']
            )
            # if the user is authenticate correctly then the login the user
            if user is not None:
                # check that user is activate or not
                if user.is_active:
                    return HttpResponse('authenticated correctly.')
                else:
                    return HttpResponse("user is un active")
            else:
                return HttpResponse("can't not find the data from the database!!")
    else:
        form = LoginForm()
        
    return render(
        request,
        'account/login.html',
        {
            'form':form
        }
    )
