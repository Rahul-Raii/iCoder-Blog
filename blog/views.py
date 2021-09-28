from django.shortcuts import render, HttpResponse, redirect
from .models import Post,comments
from django.contrib import messages
from blog.templatetags import get_dict

# Create your views here.
def blogHome(request):
    allpost= Post.objects.all()
    context= {'allpost': allpost}
    return render(request, 'blog/blogHome.html', context)
    # return HttpResponse('Hello World. Blog Home')

def blogPost(request, slug):
    allpost= Post.objects.filter(slug= slug).first()
    comment= comments.objects.filter(post= allpost, parent=None)
    replies= comments.objects.filter(post= allpost).exclude(parent=None)
    replydict= {}
    for reply in replies:
        if reply.parent.sno not in replydict.keys():
            replydict[reply.parent.sno]= [reply]
        else:
            replydict[reply.parent.sno].append(reply)
    context= {'allpost': allpost, 'comments': comment, 'replydict': replydict}
    return render(request, 'blog/blogPost.html', context)
    # return HttpResponse(f'Hello World. This is Blog Post. {slug}')

def postcomment(request):
    if request.method=='POST':
        comment= request.POST.get("comment")
        user= request.user
        postsno= request.POST.get("postsno")
        post= Post.objects.get(sno= postsno)
        parentSno= request.POST.get("parentSno")
        
        if parentSno == "":
            comment= comments(user= user, post= post, comment=comment)
            comment.save()
            messages.success(request, 'Your comment has been posted successfully')
        else:
            parent= comments.objects.get(sno=parentSno)
            comment= comments(user= user, post= post, comment=comment, parent=parent)
            comment.save()
            messages.success(request, 'Your reply has been posted successfully')
    
    return redirect(f"/blog/{post.slug}")
