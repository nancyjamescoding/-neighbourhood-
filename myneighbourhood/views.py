from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import(
    ListView
)
from .models import (
    Neighbourhood
)
from .forms import *
from django.views import generic

# Create your views here.
class NeighbourhoodListView(ListView):
    template_name = 'neighbourhoods.html'
    queryset= Neighbourhood.objects.all()
    context_object_name = 'neighbourhoods'

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


# Lamding page view
def home(request):
    if request.user.is_authenticated:
            # If a user is logged in, redirect them to a page informing them of such
        return redirect('/neighbourhoods')
    else:
        return render(request, 'home.html')


@login_required(login_url='/accounts/login/')
def profile(request):
    print(request.user.email)
    current_user = request.user
    profile = Profile.objects.all()

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES,instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return render(request,'profile.html')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form':u_form,
        'p_form':p_form,
        'user': current_user
    }

    return render(request, 'profile.html',context)


@login_required(login_url='/accounts/login/')
def addneighbourhood(request):
    neighbourform = NeighbourhoodForm()
    neighbourform.owner = request.user
    if request.method == "POST":
        neighbourform = NeighbourhoodForm(request.POST,request.FILES)
        if neighbourform.is_valid():
           neighbourform.save()
           return redirect('/neighbourhoods')
        else:
           neighbourform=NeighbourhoodForm(request.POST,request.FILES)

    return render(request,'neighbourhood_form.html',{"neighbourform":neighbourform})


def neighbourhood_details(request,neighbourhood_id):
    businesses=Business.objects.filter(neighborhood=neighbourhood_id)
    posts=Post.objects.filter(neighborhood=neighbourhood_id)
    neighbourhood=Neighbourhood.objects.get(pk=neighbourhood_id)
    return render(request,'details.html',{'neighbourhood':neighbourhood,'businesses':businesses,'posts':posts})


@login_required(login_url="/accounts/login/")
def new_business(request,pk):
    current_user = request.user
    neighborhood = get_object_or_404(Neighbourhood,pk=pk)
    if request.method == 'POST':
        business_form = NewBusinessForm(request.POST, request.FILES)
        if business_form.is_valid():
            business = business_form.save(commit=False)
            business.user = current_user
            business.neighborhood=neighborhood
            business.save()
        return redirect('detail', neighbourhood_id=neighborhood.id)

    else:
        business_form = NewBusinessForm()
    return render(request, 'new_business_form.html', {"form": business_form,'neighborhood':neighborhood})

@login_required(login_url="/accounts/login/")
def new_post(request,pk):
    current_user = request.user
    neighborhood = get_object_or_404(Neighbourhood,pk=pk)
    if request.method == 'POST':
        post_form = NewPostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = current_user
            post.neighborhood=neighborhood
            post.save()
        return redirect('detail', neighbourhood_id=neighborhood.id)

    else:
        post_form = NewPostForm()
    return render(request, 'new_post_form.html', {"form": post_form,'neighborhood':neighborhood})


def search_hoods(request):
    if 'search' in request.GET and request.GET['search']:
        search_term=request.GET.get('search')
        searched_hoods=Neighbourhood.search_by_name(search_term)
        message=f'{search_term}'

        return render(request,'search.html',{"message":message,"searched_hoods":searched_hoods})

    else:
        message='You Havent searched for any term'

        return render(request, 'search.html',{"message":message})