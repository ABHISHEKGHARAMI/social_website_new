from django.shortcuts import render , redirect , get_object_or_404
from django.contrib import messages
from .forms import ImageCreateForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import Image
# Create your views here.


# first view is the image create and save it in the database
@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST)
        # check the form is valid
        if form.is_valid():
            cd = form.cleaned_data
            new_image = form.save(commit=False)
            #  assign the user
            new_image.user = request.user
            new_image.save()
            messages.success(request,'Image Created Successfully.')
            return redirect(new_image.get_absolute_url())
    else:
        form = ImageCreateForm(data=request.GET)
        
    return render(
        request,
        'images/image/create.html',
        {
            'section':'images',
            'form':form
        }
    )
    
    
# image detail view for the image
def image_detail(request,id,slug):
    image = get_object_or_404(Image,id=id,slug=slug)
    return render(
        request,
        'images/image/detail.html',
        {
            'section':'images',
            'image' : image
        }
    )



# like image for the post with the help of the Json response
@require_POST
@login_required
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
            else:
                image.users_like.remove(request.user)
                
            return JsonResponse({'status':'ok'})
        except Image.DoesNotExist:
            pass
    return JsonResponse({'status':'error'})