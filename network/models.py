from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Post {self.id} created by {self.creator} on {self.created_at.strftime('%d %b %Y %H:%M:%S')}"


class CommentLike(models.Model):
    comment = models.ForeignKey("Comment", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"User: {self.user} | Likes Comment: {self.comment.message} | ID: {self.comment.id} | Made by: {self.comment.author}"

    
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userComment")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True, related_name="postComment")
    message = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name="likedComments", through=CommentLike)
    
    def __str__(self):
        return f"User: {self.author} | Commented on: {self.post.content} | Made by: {self.post.creator} | Created on: {self.post.created_at}"
    
    
class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userFollowing")
    user_follower = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userFollowed")
    
    def __str__(self):
        return f"{self.user} is following {self.user_follower}"


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True, related_name="postLike")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userLike")
    
    def __str__(self):
        return f"User: {self.user} | Likes: {self.post}"
    

