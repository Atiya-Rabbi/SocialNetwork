
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<str:username>/newpost", views.newpost, name="newpost"),
    path("likes/<int:postid>/<str:postadmin>/<int:flag>", views.likes, name="likes"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("postliked/<str:username>", views.postliked, name="postliked"),
    path("follow/<str:name>/<int:flag>", views.follow, name="follow"),
    path("followings/<str:name>", views.followings, name="followings"),
    path("followingpost", views.followingpost, name="followingpost"),
    path("editpost", views.editpost, name = "editpost")
]
