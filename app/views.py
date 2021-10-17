from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.core import serializers
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
import random

import json

from .models import User, Profile, Posts, Likes, Follow, Comments
from .forms import UserForm, ProfileForm, PostForm, UserUpdateForm, ProfileUpdateForm

def sidebar(request):
    #who to follow
    all_users = User.objects.all()
    all_users = all_users.exclude(username = request.user.username)
    users_following = Follow.objects.filter(follower = request.user.username).values_list('following', flat=True)
    all_users = all_users.exclude(username__in =(users_following))
    all_users = list(all_users)
    random.shuffle(all_users)
    if len(all_users) > 3:
        all_users = all_users[0:3]
    message = ""
    if not all_users:
        message="You have followed everyone"
    #trending
    trending = Posts.objects.all()
    trending = list(trending)
    random.shuffle(trending)
    if len(trending) > 2:
        trending = trending[0:2]
    return all_users, message, trending

def index(request):
    #new post form
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            form.save()
            return HttpResponseRedirect(reverse("index"))
    form = PostForm()

    #get posts
    allposts = Posts.objects.filter(post_type = "Question").order_by('-date')    
    allposts = allposts[0:2]
    #paginator
    paginator = Paginator(allposts, 5)
    page_number = request.GET.get('page')
    allposts = paginator.get_page(page_number)
    #liked posts
    liked_posts = Likes.objects.filter(user = request.user.username).values_list('post_number', flat=True)
    #sidebar
    all_users, message, trending = sidebar(request)
    #subject list
    subjects = ["Math", 'Physics', 'Chemistry', 'Biology', 'Economics', 'Accounting', 'English']
    colors = ["#ffadad", "#ffd6a5", '#fdffb6', '#caffbf', '#9bf6ff', '#a0c4ff', '#bdb2ff', '#ffc6ff', '#80ed99', '#ffcad4', '#fcf6bd']
    levels = ["Preparatory","Freshman", "Sophomore", "Junior", "Senior"]
    random.shuffle(subjects)
    return render(request, "app/index.html", {
        "form": form,
        "posts": allposts,
        "liked_posts": liked_posts,
        "whoToFollow": all_users,
        "message": message,
        "trending": trending,
        "subjects": subjects,
        "colors":colors,
        "levels": levels
    })

def all_subjects(request):
    subjects = ["Math", 'Physics', 'Chemistry', 'Biology', 'Economics', 'Accounting', 'English', 'Electrical Engineering', 'Mech. Engineering', 'Computer Science', 'Chemical Engineering', 'Ciivil Engineering', 'History', 'Geography', 'Music']
    random.shuffle(subjects)
    
    colors = ["#ffadad", "#ffd6a5", '#fdffb6', '#caffbf', '#9bf6ff', '#a0c4ff', '#bdb2ff', '#ffc6ff', '#80ed99', '#ffcad4', '#fcf6bd']
    #sidebar
    all_users, message, trending = sidebar(request)
    context = {
        'subjects': subjects,
        'colors': colors,
        "whoToFollow": all_users,
        "message": message,
        "trending": trending
    }
    
    return render(request, 'app/all_subjects.html', context)

def all_questions(request, subject):
    allposts = Posts.objects.filter(post_type = "Question", subject = subject).order_by('-date')
    #sidebar
    all_users, message, trending = sidebar(request)
    context = {
        'allposts': allposts,
        "whoToFollow": all_users,
        "message": message,
        "trending": trending,
        'subject': subject
    }
    return render(request, 'app/all_questions.html', context)

def subject_page(request, subject):
    #questions
    questions = Posts.objects.filter(post_type = "Question", subject = subject)
    #videos
    videos = Posts.objects.filter(Q(post_type = "Content Share") | Q(post_type = "File Share"), subject = subject).exclude(video = "")
    for video in videos:
        video.video = "http://www.youtube.com/embed/" + video.video.split("?v=")[1]
    #links
    files = Posts.objects.filter(Q(post_type = "Content Share") | Q(post_type = "File Share"), subject = subject).exclude(doc = "null")
    #sidebars
    all_users, message, trending = sidebar(request)
    #context
    context = {
        "subject": subject,
        "questions": questions,
        "videos": videos,
        "files": files,
        "whoToFollow": all_users,
        "message": message,
        "trending": trending
    }
    return render(request, "app/subject.html", context)

def post(request, identity):
    all_users, message, trending = sidebar(request)
    liked_posts = Likes.objects.filter(user = request.user.username).values_list('post_number', flat=True)
    post = Posts.objects.get(id = identity)
    comments = Comments.objects.filter(post = identity).order_by('-id')
    context = {
        "post": post,
        "whoToFollow": all_users,
        "message": message,
        "trending": trending,
        "liked_posts": liked_posts,
        'comments':comments
        
    }
    return render(request, "app/post.html", context)

def userdata(request, order, the_id):
    if order == "first":
        post = Posts.objects.get(id = the_id)
        guy = Profile.objects.filter(user = post.user)
        return HttpResponse(serializers.serialize("json", guy))
    elif order == "second":
        post = Posts.objects.get(id = the_id)
        guy = User.objects.filter(id = post.user.id)
        return HttpResponse(serializers.serialize("json", guy))
    elif order == "third":
        curr = request.user
        guy = Profile.objects.filter(user = curr)
        return HttpResponse(serializers.serialize("json", guy))
    elif order == "fourth":
        curr = request.user
        guy = User.objects.filter(id = curr.id)
        return HttpResponse(serializers.serialize("json", guy))



@login_required
def add_comment(request, post_id, comment):
    profiler = User.objects.get(id = request.user.id)
    add = Comments(username = request.user.username, pic = profiler.profile.profile_pic.url, post = post_id, content = comment)
    add.save()
    post = Posts.objects.get(id = post_id)
    post.comments += 1
    post.save()
    return HttpResponse(status=204)

def getcomments(request, post_id):
    comments = Comments.objects.filter(post = post_id).order_by('-id')
    return HttpResponse(serializers.serialize("json", comments))





def search(request, number, query):
    if number == "first":
        posts = Posts.objects.all()
        tings = []
        for post in posts:
            if query.lower() in post.title.lower():
                tings.append(post.id)
        posts = Posts.objects.filter(id__in=tings)
        return HttpResponse(serializers.serialize("json", posts))
        
    elif number == "second":
        everyone = User.objects.all()
        tings = []
        for person in everyone:
            if query.lower() in person.username.lower():
                tings.append(person)
        return HttpResponse(serializers.serialize("json", tings))


@login_required
def profile(request, user):
    if request.method == "POST":
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        u_form = UserUpdateForm(request.POST, instance = request.user)
        if p_form.is_valid() and u_form.is_valid():
            u_form.save()
            p_form.save()
        return redirect('profile', user = request.user.username)
        
    else:
        p_form = ProfileUpdateForm(instance=request.user, initial = {'bio': request.user.profile.bio})
        u_form = UserUpdateForm(instance=request.user.profile, initial={'username': request.user.username, 'email': request.user.email})
        #create new post form
        form = PostForm()
        # user info 
        active_user = User.objects.get(username = user)
        #user's posts
        my_posts = Posts.objects.filter(user = request.user.id).order_by('-date')
        #user's liked posts
        likes = Likes.objects.filter(user = user).values_list('post_number', flat=True)
        liked_posts = Posts.objects.filter(id__in=likes)
        #statistonks
        numFollowing = len(Follow.objects.filter(follower = user))
        numFollowers = len(Follow.objects.filter(following = user))
        #comments
        comments = Comments.objects.filter(username = user).order_by("-date")
        all_posts = Posts.objects.all()
        #sidebar
        all_users, message, trending = sidebar(request)
        #numbers
        numPosts = len(my_posts)
        numLikes = len(liked_posts)
        numComments = len(comments)
        
    return render(request, "app/profile.html", {
        'my_posts': my_posts,
        'liked_posts': liked_posts,
        'numPosts': numPosts,
        'numFollowing': numFollowing,
        'numFollowers': numFollowers,
        'active_user': active_user,
        "form": form,
        'p_form': p_form,
        'u_form': u_form,
        'comments': comments,
        'all_posts': all_posts,
        "whoToFollow": all_users,
        "message": message,
        "numLikes": numLikes,
        "numComments": numComments,
        "trending": trending
    })


@login_required
def delete(request, identity, kind):
    if kind == 'comment':
        comment = Comments.objects.get(id = identity)
        post = Posts.objects.get(id = comment.post)
        post.comments -= 1
        post.save()
        comment.delete()
        return HttpResponse(status=204)

def explore(request):
    form = PostForm()
    users = User.objects.all()
    all_users, message, trending = sidebar(request)
    return render(request, 'app/explore.html', {
        'users': users,
        "form": form,
        "whoToFollow": all_users,
        "message": message,
        "trending": trending
    })

def sort(request, sortBy, uniSort, subjectSort):
    posts = Posts.objects.all()

    if sortBy != "0":
        if sortBy == "popular":
            posts = posts.order_by("-likes")
        elif sortBy == "recent":
            posts = posts.order_by("-date")

    if subjectSort != "0":
        posts = posts.filter(subject = subjectSort)
    
    if uniSort !="0":
        posts = posts.filter(university = uniSort)

    
    return HttpResponse(serializers.serialize("json", posts))

def postmodal(request, post_id):
    post = Posts.objects.filter(id = post_id)
    return HttpResponse(serializers.serialize("json", post))

@login_required
def like(request, postid):
    try:
        liker = Likes.objects.get(user = request.user.username, post_number = postid)
    except Likes.DoesNotExist:
        post = Posts.objects.get(id = postid)
        post.likes = post.likes + 1
        post.save()
        liker = Likes(user = request.user.username, post_number = postid)
        liker.save()
        return HttpResponse(str(post.likes))
    else:
        post = Posts.objects.get(id = postid)
        post.likes = post.likes - 1
        post.save()
        liker = Likes.objects.get(user = request.user.username, post_number = postid)
        liker.delete()
        return HttpResponse(str(post.likes))

@login_required
def editpost(request, newcontent, newtitle, postid):
    post = Posts.objects.get(id = postid)
    post.desc = newcontent
    post.title = newtitle
    post.save()
    response = [post.title, post.desc]
    data = json.dumps(response)
    return HttpResponse(data)


@login_required
def addfollow(request, profile_user):
    addFollower = Follow(follower = request.user.username, following = profile_user)
    addFollower.save()
    return HttpResponseRedirect(reverse("user_page", args=(profile_user,)))

@login_required
def removefollow(request, profile_user):
    Follow.objects.filter(follower = request.user.username, following = profile_user).delete()
    return HttpResponseRedirect(reverse("user_page", args=(profile_user,)))


def user_page(request, username):
    form = PostForm()
    active_user = User.objects.get(username = username)
    posts = Posts.objects.filter(user = active_user.id).order_by('-date')
    likes = Likes.objects.filter(user = request.user.username).values_list('post_number', flat=True)
    isfollowing = Follow.objects.filter(follower = request.user.username, following = username)
    #number of following
    numFollowing = len(Follow.objects.filter(follower = username))
    #number of followers
    numFollowers = len(Follow.objects.filter(following = username))
    #number of posts
    numPosts = len(posts)
    #who to follow
    all_users = User.objects.all()
    all_users = all_users.exclude(username = request.user.username)
    users_following = Follow.objects.filter(follower = request.user.username).values_list('following', flat=True)
    all_users = all_users.exclude(username__in =(users_following))
    if len(all_users) > 3:
        all_users = all_users[0:3]
    #list of files
    filemessage = ""
    vidmessage = ""
    if numPosts == 0:
        filemessage = "@" + username + " has not uploaded any files"
        vidmessage = "@" + username + " has not uploaded any links"
    else:
        filelist = Posts.objects.filter(user = active_user.id, doc = 'null').count()
        
        if filelist:
            filemessage = "@" + username + " has not uploaded any files"
        #list of links
        videolist = Posts.objects.filter(user = active_user.id, video = '').count()
        
        if videolist:
            vidmessage = "@" + username + " has not uploaded any links"

        listlist = Posts.objects.filter(user = active_user.id, video = '', doc= 'null').count()
        if listlist:
            filemessage = ""
            vidmessage = ""
    #trending
    trending = Posts.objects.all()
    trending = list(trending)
    random.shuffle(trending)
    if len(trending) > 2:
        trending = trending[0:2]
    return render(request, "app/user.html", {
        'posts': posts,
        'active_user': active_user,
        'liked_posts': likes,
        'isfollowing': isfollowing,
        'numFollowing': numFollowing,
        'numFollowers': numFollowers,
        'numPosts': numPosts,
        "whoToFollow": all_users,
        "filemessage": filemessage,
        "vidmessage": vidmessage,
        "form": form,
        "trending": trending
    })

@login_required
def following(request):
    form = PostForm()
    users_following = Follow.objects.filter(follower = request.user.username).values_list('following', flat=True)
    users_id = User.objects.filter(username__in =(users_following)).values_list('id', flat=True)
    posts = Posts.objects.filter(user__in =(users_id)).order_by('-date')
    liked_posts = Likes.objects.filter(user = request.user.username).values_list('post_number', flat=True)
    #paginator
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    #who to follow
    all_users = User.objects.all()
    all_users = all_users.exclude(username = request.user.username)
    users_following = Follow.objects.filter(follower = request.user.username).values_list('following', flat=True)
    all_users = all_users.exclude(username__in =(users_following))
    if len(all_users) > 3:
        all_users = all_users[0:3]
    #trending
    trending = Posts.objects.all()
    trending = list(trending)
    random.shuffle(trending)
    if len(trending) > 2:
        trending = trending[0:2]
    return render(request, "app/following.html", {
        'posts': posts,
        'liked_posts': liked_posts,
        "whoToFollow": all_users,
        "form": form,
        "trending": trending
    })

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
            return render(request, "app/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        all_users, message, trending = sidebar(request)
        return render(request, "app/login.html", {
        "whoToFollow": all_users,
        "message": message,
        "trending": trending
        })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        #get input from user
        username = request.POST["username"]
        email = request.POST["email"]
        bio = request.POST["bio"]
        profile_pic = request.FILES.get("profile_pic", False)
        uni = request.POST.get("uni", "No Uni")

        pic = FileSystemStorage()
        pic_url = pic.save(profile_pic.name, profile_pic)
        location = pic.url(pic_url)

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "app/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.profile.bio = bio
            user.profile.uni = uni
            user.profile.profile_pic = profile_pic
            user.save()
        except IntegrityError:
            return render(request, "app/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        all_users, message, trending = sidebar(request)

        return render(request, "app/register.html", {
        
        "whoToFollow": all_users,
        "message": message,
        "trending": trending
        })


