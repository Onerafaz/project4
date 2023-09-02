from django.contrib import admin
from .models import Post, User, Comment, Like, Follow, CommentLike

# Register your models here.
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Follow)
admin.site.register(CommentLike)
