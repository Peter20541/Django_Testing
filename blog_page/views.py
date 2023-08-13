
from .models import Post
from .forms import Create_PostForm,Update_post
from django.shortcuts import render,redirect,HttpResponse
from .forms import UserRegisterForm,UserLoginForm,UserUpdateForm,UserPicUpdateForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger




def home(request):
    if request.method == 'POST':
        seached_form = request.POST.get('input-search')
        blogs = Post.objects.filter(content__contains = seached_form).order_by('-date_posted')
        page = request.GET.get('page')

        paginator = Paginator(blogs,5)
        try:
            pages = paginator.page(page)
            print(pages.next_page_number())
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        
        
        if blogs.count() == 0:
            context = {'posts':pages}
            return render(request,'blog_page/home.html',context)
    else:
        blogs = Post.objects.all().order_by('-date_posted')
        page = request.GET.get('page',1)
        paginator = Paginator(blogs,5)
        try:
            pages = paginator.page(page)
            print(pages.next_page_number())
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        
    context = {'posts':pages}
    return render(request,'blog_page/home.html',context)


@login_required
def post_detail(request,pk):
    blog_detail = Post.objects.get(id = pk)

    context = {'post_detail':blog_detail}
    return render(request,'blog_page/post_detail.html',context)


@login_required
def user_create_post(request):
    form = Create_PostForm()
    if request.method == 'POST':
        form = Create_PostForm(request.POST)
        
        if form.is_valid():
            form.instance.author = request.user # Setting the author to be the currently logged in user
            form.save()
            # def get_absolute_url(self):
            # return reverse('/')
            # use reverse in the model instead of using redirect()
            return redirect('/')
        
    return render(request,'blog_page/create_post.html',{'form':form})

@login_required
def delete_post(request,pk):
    posts = Post.objects.get(id= pk)
    if posts.author == request.user:
        if request.method =='POST':
            posts.delete()
            return redirect('/')
        context = {'post_detail':posts}
        return render(request,'blog_page/delete_post.html',context)
    else:
        return HttpResponse(' <h1> Sorry You cant access this page </h1>')
    

@login_required
def update_post(request,pk):
    posts = Post.objects.get(id= pk)
    if posts.author == request.user:
        form = Update_post(instance=posts)
        if request.method =='POST':
            form = Update_post(request.POST,instance=posts)
            if form.is_valid():
                form.save()
                return redirect('home-page')
    else:
        return HttpResponse(' <h1> Sorry You cant access this page </h1>')
    return render(request,'blog_page/update_post.html',{'form':form})





# MAKE SURE THAT THE FORM COMES BEFORE AND  AFTER IF REQUEST.METHOD == POST: AND MAKE SURE TO ADD THE REQUEST.POST TO THE FORM
def user_register(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        form = UserRegisterForm()
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                user = form.cleaned_data.get('username')
                form.save(commit=True)
                message = messages.success(request,f'Account for  {user}  was created succesfully')
                return redirect('login-page')
        context = {'form':form}
        return render(request,'blog_page/register.html',context)


def user_login(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        form = UserLoginForm()
        print(request.method)
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password1')

            user = authenticate(request,username = username,password = password)
            if user is not None:
                login(request,user)
                return redirect('/')
            else:
                messages.info(request,'The Username Or Password is incorrect')
        context = {'form':form}
        return render(request,'blog_page/login.html',context)

def user_logout(request):
    logout(request)
    return redirect('login-page')

@login_required
# To add text to esting form 
def user_profile(request):
 
    if request.method == 'POST':
        user_email_update = UserUpdateForm(request.POST,instance=request.user)# request.user alread have info on login user like username and email
        image_update = UserPicUpdateForm(request.POST,request.FILES,instance=request.user.image)# request.user alread have info on login user like image
        
        if user_email_update.is_valid() and image_update.is_valid():
            user_email_update.save()
            image_update.save()
            message = messages.success(request,' Account was updated succesfully ')
    else:
        user_email_update = UserUpdateForm(instance=request.user)# request.user alread have info on login user like username and email
        image_update = UserPicUpdateForm(instance=request.user.image)# request.user alread have info on login user like image
        
    context = {
        'user_email_update':user_email_update,
        'image_update':image_update
    }
    return render(request,'blog_page/profile.html',context)




