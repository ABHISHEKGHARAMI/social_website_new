from django.shortcuts import render , redirect , get_object_or_404
from django.contrib import messages
from .forms import ImageCreateForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import Image
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
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





# image list for the user
@login_required
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images,8)
    page = request.GET.get('page')
    images_only = request.GET.get('images_only')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        if images_only:
            return HttpResponse('')
        images = paginator.page(paginator.num_pages)
        
    if images_only:
        return render(
            request,
            'images/image/list_images.html',
            {
                'section':'images',
                'images':images
            }
        )
        
    return render(
        request,
        'images/image/list.html',
        {
            'section':'images',
            'images':images
        }
    )