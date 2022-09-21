import os
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Feed, Comment, Hide_Feed, User, Like, News, Comment_Like, Comment_Comment, Hide_Feed
from uuid import uuid4
from FB_clone.settings import MEDIA_ROOT
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
#########
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import re

class Main(APIView):
    def get(self, request):    
        feed_list = Feed.objects.order_by('-created_at')
        username = request.session['username']
        user = User.objects.filter(username=username).first()

        hide_feed_list = Hide_Feed.objects.filter(username=username)
        if hide_feed_list:
            for hide_feed in hide_feed_list:
                feed_list = feed_list.exclude(id=hide_feed.feed) # Exclude hidden feed (Delete X)
        
        for feed in feed_list:
            like_count = Like.objects.filter(feed=feed.id, is_like=True).count() # How many likes
            like_or_not = Like.objects.filter(feed=feed.id, is_like=True, username=username).count() # Whether I liked or not (1 or 0)
            feed.like_count = like_count
            feed.like_or_not = like_or_not
            for comment in feed.comment_set.all():
                comment_like_count = Comment_Like.objects.filter(comment=comment.id, is_like=True).count()
                comment_like_or_not = Comment_Like.objects.filter(comment=comment.id,  username=username, is_like=True).count()
                comment.comment_like_count = comment_like_count
                comment.comment_like_or_not = comment_like_or_not
                comment.save()
        
        context = {'feed_list': feed_list, 'user':user}
        return render(request, 'main.html', context)

class Upload(APIView):
    def post(self, request):
        username = request.session['username']
        profileimg = User.objects.get(username=username).profileimg
        name = User.objects.get(username=username).name
        content = request.data.get('content', None) # Only Texts that are about to be uploaded

        if request.FILES:   # Only Picture that is about to be uploaded
            file = request.FILES['file']
            uuid_name = uuid4().hex # Random name created
            save_path = os.path.join(MEDIA_ROOT, uuid_name) # Save Random name(uuid_name) in the root inputted in setting.py
            with open(save_path,'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            contentimg = uuid_name
            Feed.objects.create(username=username, content=content, contentimg=contentimg, profileimg=profileimg, name=name)
            return Response(status=200)
        
        Feed.objects.create(username=username, content=content, profileimg=profileimg, name=name)
        return Response(status=200)

class Uploadcomment(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        comment_content = request.data.get('comment_content', None)
        username = request.session['username']
        name = User.objects.get(username=username).name

        Comment.objects.create(feed_id=feed_id, comment_content=comment_content, username=username, name=name)
        return Response(status=200)

class UploadComment_Comment(APIView):
    def post(self, request):
        comment_id = request.data.get('comment_id', None)
        comment_comment_content = request.data.get('comment_comment_content', None)
        username = request.session['username']
        name = User.objects.get(username=username).name

        Comment_Comment.objects.create(comment_id=comment_id, comment_comment_content=comment_comment_content, username=username, name=name)
        return Response(status=200)

class Share(APIView):
    def post(self, request):
        username = request.session['username']
        profileimg = User.objects.get(username=username).profileimg
        name = User.objects.get(username=username).name

        feed_id = request.data.get('feed_id')
        feed_name = request.data.get('feed_name')
        feed_content = request.data.get('feed_content', None)
        feed_contentimg = request.data.get('feed_contentimg', None)
        created_at = request.data.get('created_at')
        modified_at = request.data.get('modified_at')

        if not modified_at == 'None':   # If It was modified before ('None' was delivered in the form of character)
            Feed.objects.create(username=username, name=name, profileimg=profileimg, shared_content_id=feed_id,
            shared_feed_name=feed_name, shared_created_at=modified_at, content=feed_content, contentimg=feed_contentimg)
        else :
            Feed.objects.create(username=username, name=name, profileimg=profileimg, shared_content_id=feed_id,
            shared_feed_name=feed_name, shared_created_at=created_at, content=feed_content, contentimg=feed_contentimg)
        
        return Response(status=200)

class Modify(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id')
        content = request.data.get('content', None) # Only Texts that are about to be modified
        feed = Feed.objects.get(id=feed_id)

        if request.session['username'] != feed.username:    # If Feed-maker and Login-user are different
            return render(request, 'main.html', status=404)

        if request.FILES: # Only Picture that is about to be uploaded newly
            file = request.FILES['file']
            uuid_name = uuid4().hex
            save_path = os.path.join(MEDIA_ROOT, uuid_name)
            with open(save_path,'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            contentimg = uuid_name

            feed.content = content
            feed.contentimg = contentimg
            feed.modified_at = timezone.now()
            feed.save()
            return Response(status=200)

        feed.content = content
        feed.modified_at = timezone.now()
        feed.save()
        return Response(status=200)

class Delete(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id')
        feed = Feed.objects.get(id=feed_id)
        if request.session['username'] != feed.username:
            return render(request, 'main.html', status=404)
        feed.delete()
        return Response(status=200)

class Hide(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id')
        feed = Feed.objects.get(id=feed_id)
        username = request.session['username']
        if username == feed.username:
            return render(request, 'main.html', status=404)
        Hide_Feed.objects.create(username=username, feed=feed_id)
        return Response(status=200)
        

class TogleLike(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        likeicons = request.data.get('likeicons', None)

        if likeicons == "material-icons" : # If the likeicon is filled with black (namely If liked)
            is_like = True # Like
        else:
            is_like = False # Non-like

        username = request.session.get('username',None)
        like = Like.objects.filter(feed=feed_id, username=username).first()

        if like:
            like.is_like = is_like # Input if the login-user liked or not
            like.save()
        else:
            Like.objects.create(feed=feed_id, is_like=is_like, username=username) # First time click

        return Response(status=200)

class TogleCommentLike(APIView):
    def post(self, request):
        comment_id = request.data.get('comment_id', None)
        like_or_not = request.data.get('like_or_not', None)

        if like_or_not == "Liked" :
            is_like = True
        else:
            is_like = False

        username = request.session.get('username',None)
        comment_like = Comment_Like.objects.filter(comment=comment_id, username=username).first()

        if comment_like:
            comment_like.is_like = is_like
            comment_like.save()
        else:
            Comment_Like.objects.create(comment=comment_id, is_like=is_like, username=username)

        return Response(status=200)

class Signup(APIView):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        email = request.data.get('email', None)
        username = request.data.get('username', None)
        name = request.data.get('name', None)
        password = request.data.get('password', None)
        password2 = request.data.get('password2', None)
        if not password == password2:   # If password and password-confirm are different,
            context = {'alert': 'The passwords are not matched'}  
            return render(request, 'signup.html', context, status=400)

        for one_user in User.objects.all():
            if username == one_user.username: # If the username already exists,
                context = {'alert': 'The username already exists'}    
                return render(request, 'signup.html', context, status=400)

        User.objects.create(email=email,
                            username=username,
                            name=name,
                            password=make_password(password), # Encryption of passwords in one-way with 'make_password'
                            profileimg='default_profile') # Default profile set

        return render(request, 'login.html', status=200)

class Login(APIView):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        username = request.data.get('username', None)
        password = request.data.get('password', None)

        user = User.objects.filter(username=username).first()

        if user is None:
            return Response(status=400) # If such User doesn't exist in database,

        if user.check_password(password):
            request.session['username'] = username # login-Username will be User 
            return Response(status=200) # Login succsess
        else:
            return Response(status=400) # If Password is wrong,

class Logout(APIView):
    def get(self, request):
        request.session.flush()
        return render(request, "Login.html")

class NewsArticles(APIView):
    def get(self, request):

        def create_soup(url) : # Neccesary frame for bs4, requests
            res = requests.get(url)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, 'lxml')
            return soup

        def headline_news() :
            url = "https://www.houstonchronicle.com/" # Houston local news site
            soup = create_soup(url)
            news_list = soup.find_all("div", attrs={"class":re.compile("^corePackage--item-group")})

            n = 0
            for news in news_list :
                title = news.find("div", attrs={"class":re.compile("^corePackage--item-header")}).find("a", attrs={"class":re.compile("^hdn")})
                link = news.find("div", attrs={"class":re.compile("^corePackage--item-img")})
                picture = news.find("div", attrs={"class":re.compile("^corePackage--item-img")})
                
                if title == None or link == None :
                    continue
                n += 1
                if n == 21 or n == 22:
                    continue

                title = title.get_text().strip()
                link = link.a.attrs['href']
                picture = picture.find("a", attrs={"class":re.compile("^hdn")}).find("picture", attrs={"class":re.compile("^oneOne")})

                if link.startswith("https") and not picture is None : # If a picture exist and the link is full-link
                    News.objects.create(title=title, link=link, picture=picture.img.attrs['data-src']) 

                elif not picture is None:  # If a picture exist and the link is not full-link
                    News.objects.create(title=title, link="https://www.houstonchronicle.com{}".format(link), picture=picture.img.attrs['data-src']) 

        username = request.session['username']
        user = User.objects.filter(username=username).first()
        
        news_search = request.GET.get('news_search', None) # Search function ('None' is default, without using search)
        if news_search:
            news_list = News.objects.filter(title__icontains=news_search)
            
        else :
            News.objects.all().delete() # Delete all news, Whenever accsessed to the news page to update them
            headline_news()
            news_list = News.objects.all()

        date = datetime.now().date()
        weekday = datetime.now().weekday()
        if weekday == 0:
            weekday = 'Mon'
        elif weekday == 1:
            weekday = 'Tue'
        elif weekday == 2:
            weekday = 'Wed'
        elif weekday == 3:
            weekday = 'Thu'
        elif weekday == 4:
            weekday = 'Fri'
        elif weekday == 5:
            weekday = 'Sat'
        elif weekday == 6:
            weekday = 'Sun'

        context = {'user':user, 'news_list':news_list, 'date':date, 'weekday':weekday, 'news_search':news_search}
        return render(request, "news.html", context)
    

        
        
