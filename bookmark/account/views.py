from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse , JsonResponse
from django.contrib.auth import authenticate,login, get_user_model
from .forms import LoginForm , UserRegistrationForm , UserEditForm , ProfileEditForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile, Contact
from django.views.decorators.http import require_POST
from actions.utils import create_action
from actions.models import Actions



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
    # exclude  current user from user activity and see other activity
    actions = Actions.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list(
        'id',flat=True
    )
    if following_ids:
        #if user follow other then only retrive the user follows
        actions = actions.filter(user_id__in=following_ids)
    actions = actions.select_related(
        'user','user__profile').prefetch_related('target')[:10]
    return render(
        request,
        'account/dashboard.html',
        {
            'section':'dashboard',
            'actions':actions
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
            create_action(new_user,'has created account')
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
    
    
# user model
User = get_user_model()


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(
        request,
        'account/user/list.html',
        {
            'section':'people',
            'users' : users
        }
    )
    
    
@login_required
def user_detail(request,username):
    user = get_object_or_404(User,username=username,is_active=True)
    return render(
        request,
        'account/user/detail.html',
        {
            'section':'people',
            'user':user
        }
    )
    
#  follow and un follow system
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(
                    user_from=request.user,
                    user_to = user
                )
                create_action(request.user,'is following',user)
            else:
                Contact.objects.filter(
                    user_from = request.user,
                    user_to = user
                ).delete()
            return JsonResponse({'status':'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status':'error'})
    return JsonResponse({'status':'error'})