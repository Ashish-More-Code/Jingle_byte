from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from datetime import datetime
from django.db.models import Count,Q
from blogapp.models import Recipepost,Like,comments
from django.contrib.postgres.search import (SearchVector, SearchQuery ,SearchRank ,TrigramSimilarity)


# Create your views here.

def home(request):
    search=request.GET.get('search')
    context = {}
    if not search:
        u = Recipepost.objects.filter(is_active=True)
        trending_posts = Recipepost.objects.filter(is_active=True).order_by('-likecount')
        context['trending'] = trending_posts  
        
    else:
        vector=SearchVector(
            'title',
            'content',
        )
        query = SearchQuery(search)
        u= Recipepost.objects.annotate(rank=SearchRank(vector, query)).order_by("-rank").filter(Q(rank__gt=0) & Q(is_active=True))        
    
    context['data'] = u
    return render(request,'index.html',context)



def about(request):
    return render(request,'about.html')

def account(request):
    uid=request.user.id
    u=Recipepost.objects.filter(userid=uid)
    context={}
    context['TotalB']=len(u)
    count=0
    for i in u:
        count=count+i.likecount
    context['LikeCount']=count
    return render(request,'account.html',context)

def handleComment(request,bid):
    if request.user.is_authenticated:
        u=request.user.id
        detailblogpost=Recipepost.objects.filter(id=bid)
        comm=comments.objects.filter(bid=bid)
        context={}
        context['data']=detailblogpost
        context['comments']=comm
        if request.method=='POST':
            uid=User.objects.filter(id=u)
            recipe_post = Recipepost.objects.get(id=bid) 
            comment=request.POST['comm']
            if comment=="":
                context['errc']="Comments cannot be empty!"
                return render(request,'bdetailfromhome.html',context)
            else:
                u=comments.objects.create(uid=uid[0],bid=recipe_post,comment=comment)
                u.save()
                return render(request,'bdetailfromhome.html',context)
        else:
            return render(request,'bdetailfromhome.html',context)
    else:
        return redirect('/login')


def bdetailshome(request,bid):
    myblog=Recipepost.objects.filter(id=bid)
    comm=comments.objects.filter(bid=bid)
    context={}
    context['data']=myblog
    context['comments']=comm
    return render(request,'bdetailfromhome.html',context)

def fetchCategory(request,cat):
    context={}
    search=request.GET.get('search')
    myblog=Recipepost.objects.filter(Q(type=cat)&Q(is_active=True))
    if not search:
        
        context['cat']=myblog
        if not context['cat']:
            context['nodatafoundmsg']="No posts available in this category yet. We’re working on bringing you fresh content soon!"
            return render(request,'index.html',context)
        else:
            return render(request,'index.html',context)
    else:

        vector=SearchVector(
            'title',
            'content',
        )
        query = SearchQuery(search)
        u= Recipepost.objects.annotate(rank=SearchRank(vector, query)).order_by("-rank").filter(Q(rank__gt=0) & Q(is_active=True))     
        context['cat']=u   
        return render(request,'index.html',context)
    

def like(request,bid):
    if request.user.is_authenticated:
        uid=request.user.id 
        u=User.objects.filter(id=uid)
        bpost=Recipepost.objects.filter(id=bid)
        comm=comments.objects.filter(bid=bid)

        if bpost and u:
            like = Like.objects.filter(Recipepost=bpost[0], user=u[0]).first()
            if like:
                like.delete()
                bpost[0].likecount -= 1
                bpost[0].save()
            else:
                Like.objects.create(Recipepost=bpost[0], user=u[0])
                bpost[0].likecount += 1
                bpost[0].save()

        context={}
        #added comment
        context['comments']=comm
        context['data']=bpost
        return render(request,'bdetailfromhome.html',context)
    else:
        return render(request,'login.html')


def registration(request):
    if request.method=='POST':
        uname=request.POST['username']
        email=request.POST['email']
        upass=request.POST['pass']
        ucpass=request.POST['cpass'] 
        if uname=="" or email=="" or upass=="" or ucpass=="":
            context={}
            context['errmsg']="Username and Password can not be empty"
            return render(request,'registration.html',context)
        elif upass != ucpass:
            context={}
            context['errmsg']="Password and confirm password does not match"
            return render(request,'registration.html',context)
        else:
            try:
                u=User.objects.create(username=uname,password=upass,email=email)
                u.set_password(upass)
                u.save()
                context={}
                context['successmsg']="Registration successful"
                return render(request,'registration.html',context)
            except Exception:
                context={}
                context['errmsg']="User with this username already exists!"
                return render(request,'registration.html',context)
    else:
        return render(request,'registration.html')

def ulogin(request):
    if request.method=="POST":
        uname=request.POST['uname']
        upass=request.POST['upass']
        user = authenticate(username=uname, password=upass)
        if uname=="" or upass=="":
            context={}
            context['errmsg']="First enter the username and password"
            return render(request,'login.html',context)
        elif user is not None:
            context={}
            context['successmsg']="Login successful"
            login(request,user)
            return redirect('/')
        else:
            context={}
            context['errmsg']="Invalid username and password!"
            return render(request,'login.html',context)
    else:
        return render(request,'login.html')
    
def ulogout(request):
    logout(request)
    return redirect('/')

def createblog(request):
    uid=request.user.id
    u=User.objects.filter(id=uid)
    if request.method=='POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        date = datetime.now()
        type=request.POST.get('category')
        pimage = request.FILES.get('pimage')

        if title=="" or content=="" or content=="" or date=="" or pimage=="":
            context={}
            context["errmsg"]="All fields are mandatory !"
            return render(request,'createblog.html',context)
        else:
            context={}
            u=Recipepost.objects.create(userid=u[0],title=title,content=content,createdate=date,pimage=pimage,type=type)
            u.save()
            context['successmsg']='Great job! Your blog post is now live.'
            return render(request,'createblog.html',context)
    else:
        return render(request,'createblog.html')
    
def myblogs(request):
    uid=request.user.id
    u=User.objects.filter(id=uid)
    myblog=Recipepost.objects.filter(userid=u[0])
    context={}
    context["data"]=myblog
    return render(request,'myblogs.html',context)

def deletepost(request,bid):
    myblog=Recipepost.objects.filter(id=bid)
    print(myblog)
    myblog.delete()
    context={}
    context['data']=myblog
    return redirect('/myblogs')
    

def detailedblog(request,bid):
    myblog=Recipepost.objects.filter(id=bid)
    comm=comments.objects.filter(bid=bid)
    context={}
    context['data']=myblog
    context['comments']=comm
    return render(request,'detailedblog.html',context)
    
def editblog(request,bid):
    if request.method=="GET":
        myblog=Recipepost.objects.filter(id=bid)
        context={}
        context['data']=myblog
        return render(request,'editblog.html',context)
    else:
        title=request.POST['title']
        content=request.POST['content']
        if title=="" or content=="":
            myblog=Recipepost.objects.filter(id=bid)
            context={}
            context['data']=myblog
            context["errmsg"]="All fields are mandatory and cannot be empty !"
            return render(request,'editblog.html',context)
        else:
            Recipepost.objects.filter(id=bid).update(title=title, content=content)
            myblog=Recipepost.objects.filter(id=bid)
            context={}
            context['data']=myblog
            context['successmsg']="Blog Post Edited"
            return render(request,'editblog.html',context)


