
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newPost", views.new_post, name="newPost"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("unfollow", views.unfollow, name="unfollow"),
    path("follow", views.follow, name="follow"),
    path("following", views.following, name="following"),
    path("edit/<int:post_id>", views.edit, name="edit"),
    path("removelike/<int:post_id>", views.removeLike, name="removelike"),
    path("addlike/<int:post_id>", views.addLike, name="addlike"),
    path("addNewComment/<int:id>", views.addComment, name="addComment"),
    path('search/', views.search, name='search'),
    path('addCommentLike/<int:comment_id>/', views.like_comment, name='addCommentLike'),
    path('removeCommentlike/<int:comment_id>/', views.like_comment, name='removeCommentLike'),

]
