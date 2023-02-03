from django.urls import path
from .views import *

urlpatterns = [
    path('main/', Main.as_view(), name='main'),
    path('main/upload', Upload.as_view(), name='upload'),
    path('main/share/', Share.as_view(), name='share'),
    path('main/modify/', Modify.as_view(), name='modify'),
    path('main/delete/', Delete.as_view(), name='delete'),
    path('main/hide/', Hide.as_view(), name='hide'),
    path('uploadcomment/', Uploadcomment.as_view(), name='uploadcomment'),
    path('uploadcomment_comment/', UploadComment_Comment.as_view(), name='uploadcomment_comment'),
    path('toglelike/', TogleLike.as_view(), name='toglelike'),
    path('toglecommentlike/', TogleCommentLike.as_view(), name='toglecommentlike'),
    path('news/', NewsArticles.as_view(), name='news'),

    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
]
