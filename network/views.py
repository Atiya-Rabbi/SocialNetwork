from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import datetime
import operator
import json
from django import forms
from .models import * 
from django.http import Http404
from django.core.paginator import Paginator

#working correctly
def index(request):
    flag = 0
    if request.user.is_authenticated:
        username = User.objects.get(username = request.user.username)
    else:
        username = ""
    page_obj = pagination(request)
    return render(request, "network/index.html", {
        'page_obj': page_obj,
        "username": username,
        "flag": flag,
        })

def followingpost(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            flag = 1
            u = User.objects.get(username=request.user.username)
            f = Following.objects.get(username = u)
            page_obj = pagination(request)
            return render(request, "network/index.html",{
                "page_obj": page_obj,
                "following": f.following.all(),
                "flag": flag,
                })
        else:
            return HttpResponseRedirect(reverse("index"))

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

#working correctly
def newpost(request, username):
    if request.method == "POST":
        allpost = Allpost()
        allpost.post = request.POST["newpost"]
        u = User.objects.get(username= username)
        allpost.postadmin = u
        date = datetime.datetime.now()
        #format the date
        allpost.postdate = date.strftime("%B %d, %Y, %I:%M%p")
        #a newly created post has 0 likes
        allpost.likes = 0
        allpost.save()
    return HttpResponseRedirect(reverse("index"))

#working correctly
def likes(request, postid, postadmin, flag):
    if request.method == "GET":
        if request.user.is_authenticated:
            u = User.objects.get(username=request.user.username)
            try:
                if Post_liked.objects.get(username = u):
                    pass
            except:
                pl = Post_liked()
                pl.username = u
                pl.save()
            pp = Post_liked.objects.get(username=u)
            p = Allpost.objects.get(id = postid)
            
            no_likes = p.likes
            if flag == 0:
                p.likes = no_likes + 1
                p.save()
                pp.postliked.add(p)
                pp.save()
                return HttpResponse("liked")
            elif flag == 1:
                p.likes = no_likes - 1
                p.save()
                pp.postliked.remove(p)
                pp.save()
                return HttpResponse("no like")
        else:
            return HttpResponseRedirect(reverse("index"))

#working correctly
def postliked(request, username):
    if request.method == "GET":
        if request.user.is_authenticated:
            postid = []
            u = User.objects.get(username=username)
            try:
                if Post_liked.objects.get(username = u):
                    post_liked = Post_liked.objects.get(username = u)
                    t = post_liked.postliked.all()
                    for p in t:
                        postid.append(p.id)
                    print(postid)
                    postid_as_json = json.dumps(postid)
                    return HttpResponse(postid_as_json)
            except:
                return HttpResponse("no likes")
        else:
            return HttpResponseRedirect(reverse("index"))

#working correctly
def profile(request, username):
    if request.method == "GET":
        if request.user.is_authenticated:
            flag = 0
            u = User.objects.get(username=username)
            if request.user.username == username:
                flag = 1
            try:
                f = Follower.objects.get(username=u)
                f1 = f.follower.count()
            except:
                f1 = 0
            try:
                f = Following.objects.get(username=u)
                f2 = f.following.count()
            except:
                f2 = 0
            return render(request, "network/profile.html", {
                "username": username,
                "allpost": Allpost.objects.filter(postadmin=u),
                "flag": flag,
                "follower": f1,
                "following": f2
                })
        else:
            return HttpResponseRedirect(reverse("index"))
#working correctly
def follow(request, name, flag):
    if request.method == "GET":
        if request.user.is_authenticated:
            f1 = Following()
            f2 = Follower()
            u1 = User.objects.get(username=request.user.username)
            try:
                u2 = User.objects.get(username=name)
                try:
                    if Following.objects.get(username=u1):
                        pass
                except:
                    f1.username = u1
                    f1.save()
                try:
                    if Follower.objects.get(username=u2):
                        pass
                except:
                    f2.username = u2
                    f2.save()
                f11 = Following.objects.get(username=u1)    
                f22 = Follower.objects.get(username=u2)
                if flag ==0:
                    f11.following.add(u2)
                    f22.follower.add(u1)
                    f11.save()
                    f22.save()
                    return HttpResponse("following")
                elif flag == 1:
                    f11.following.remove(u2)
                    f22.follower.remove(u1)
                    f11.save()
                    f22.save()
                    return HttpResponse("not following")
            except:
                return HttpResponse("not following")
        else:
            return HttpResponseRedirect(reverse("index"))

#working correctly
def followings(request, name):
    if request.method == "GET":
        if request.user.is_authenticated:
            try:
                u1 = User.objects.get(username = request.user.username)
                obj = Following.objects.get(username = u1)
                u2 = User.objects.get(username=name)
                if u2 in obj.following.all():
                    return HttpResponse("Yes")
                else:
                    return HttpResponse("No")
            except:
                return HttpResponse("No")
        else:
            return HttpResponseRedirect(reverse("index"))

def editpost(request):
    if request.method == "POST":
        if request.user.username == request.POST.get('admin'):
            postid = request.POST.get('id')
            editedpost = request.POST.get('post')
            p = Allpost.objects.get(id=postid)
            p.post = editedpost
            p.save()
            return HttpResponse("successful")
        else:
            raise Http404
    return HttpResponse("unsuccessful Attempt")

def pagination(request):
    allpost = Allpost.objects.all().order_by('-id')
    paginator = Paginator(allpost, 10) # Show 10 posts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj