from django.shortcuts import render, HttpResponse, redirect
from home.models import contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from blog.models import Post

# Create your views here.
def home(request):
    allpost= Post.objects.all()
    context= {'allpost': allpost}
    return render(request, 'home/home.html', context)

def about(request):
    return render(request, 'home/about.html')
    # return HttpResponse('Hello World. This is About')

def contac(request):
    if request.method=='POST':
        name= request.POST['name']
        email= request.POST['email']
        phone= request.POST['phone']
        content= request.POST['content']
        print(name, email, phone, content)
        if len(name)==0 or len(phone)<10:
            messages.error(request, 'Please Enter  valid information !!')
        else:
            Contact=contact(name=name, email=email, phone=phone, content=content)
            Contact.save()
            messages.success(request, 'Your message have been successfully send !!')
    return render(request, 'home/contact.html')
    # return HttpResponse('Hello World. This is Contact')

def search(request):
    query= request.GET['query']
    if len(query)>100:
        allpost= Post.objects.none()
    else:
        allpostblog= Post.objects.filter(title__icontains= query)
        allpostcontent= Post.objects.filter(content__icontains= query)
        allpostauthor= Post.objects.filter(author__icontains= query)
        allpost= allpostblog.union(allpostcontent).union(allpostauthor)
    if allpost.count()==0:
        messages.warning(request, 'No Search Results Found. Please refine your query')
    params= {'allpost': allpost, 'query': query}
    return render(request, 'home/search.html', params)

def signup(request):
    if request.method=='POST':
        username= request.POST['username']
        fname= request.POST['fname']
        lname= request.POST['lname']
        email= request.POST['email']
        pass1= request.POST['pass1']
        pass2= request.POST['pass2']

        # check 
        if len(username)>10:
            messages.alret(request, 'Your usename must be under 10 character')
            return redirect('/')
        if not username.isalnum():
            messages.alret(request, 'Your usename must be character and number only')
            return redirect('/')
        if pass1!=pass2:
            messages.warning(request, 'Must write same password')
            return redirect('/')

        # making signup table 
        myuser= User.objects.create_user(username, email, pass1)
        myuser.first_name= fname
        myuser.last_name= lname
        myuser.save()
        messages.success(request, 'Your account has been successfully created')
        return redirect('/')
    else:
        return HttpResponse('Not successfull')

def loginn(request):
    if request.method=="POST":
        username = request.POST['loginusername']
        password = request.POST['pass']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            messages.success(request, 'Successfully Logged_in')
            return redirect('/')
        else:
            # Return an 'invalid login' error message.
            messages.error(request, 'Error in login !! Wrong Password')
            return redirect('/')
    return HttpResponse('404 Not Found')

def logoutt(request):
    logout(request)
    # Redirect to a success page.
    messages.success(request, 'Successfully Logged out')
    return redirect('/')