from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json


from .models import User, Like, Post, Comment, Follow, CommentLike



def index(request):
    posts = Post.objects.all().order_by("-created_at")
    
    # Pagination
    paginator = Paginator(posts, 10)
    pageNumber = request.GET.get('page')
    pagePosts = paginator.get_page(pageNumber)
    
    whoYouLikedPosts = []
    whoYouLikedComments = []
    
    if request.user.is_authenticated:
        # Get posts liked by the user
        post_likes = Like.objects.filter(user=request.user)
        whoYouLikedPosts = [like.post.id for like in post_likes]

        # Get comments liked by the user
        comment_likes = CommentLike.objects.filter(user=request.user)
        whoYouLikedComments = [like.comment.id for like in comment_likes]
        
    return render(request, "network/index.html", {
        "pagePosts": pagePosts,
        "whoYouLiked": whoYouLikedPosts,
        "whoYouLikedComments": whoYouLikedComments,
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


@login_required
def new_post(request):
    current_user = request.user

    # Create a new post
    if request.method == "POST":
        content = request.POST["content"]
        
        
        new_post = Post(
            creator = current_user,
            content = content
        )
        
        # Save the post into DB
        new_post.save()
                
        return HttpResponseRedirect(reverse(index))


def posts(request, id): 
    # Display user, posts, comments and likes
    isCreator = request.user.username == postData.creator.username
    postData = Post.objects.get(pk=id)
    allComments = Comment.objects.filter(post=postData)
    likes_count = Like.objects.filter(post=postData).count()
    
    whoYouLiked = []  # Initialize the list

    # Check if the user is authenticated before calculating likes
    if request.user.is_authenticated:
        likes_by_user = Like.objects.filter(post=postData, user=request.user)
        whoYouLiked = [like.post.id for like in likes_by_user]
                    
    return render(request, "network/posts.html", {
        "posts": postData,
        "isCreator": isCreator,
        "allComments": allComments,
        "likes": likes_count,
        "whoYouLiked": whoYouLiked
    })
    

def profile(request, user_id):
    user = User.objects.get(pk=user_id)
    posts = Post.objects.filter(creator=user).order_by("id").reverse()
    
    # Pagination
    paginator = Paginator(posts, 10)
    pageNumber = request.GET.get('page')
    pagePosts = paginator.get_page(pageNumber)
    
    # Followers
    following = Follow.objects.filter(user=user)
    followers = Follow.objects.filter(user_follower=user)
    
    # Following others and not own
    try:
        checkFollow = followers.filter(user=User.objects.get(pk=request.user.id))
        if len(checkFollow) != 0:
            isFollowing= True
        else:
            isFollowing = False
    except:
        isFollowing = False
        
        
    whoYouLikedPosts = []
    whoYouLikedComments = []

    if request.user.is_authenticated:
        # Get posts liked by the user
        post_likes = Like.objects.filter(user=request.user)
        whoYouLikedPosts = [like.post.id for like in post_likes]

        # Get comments liked by the user
        comment_likes = CommentLike.objects.filter(user=request.user)
        whoYouLikedComments = [like.comment.id for like in comment_likes]
    
    return render(request, "network/profile.html", {
        "posts": posts,
        "pagePosts": pagePosts,
        "username": user.username,
        "following": following,
        "followers": followers,
        "isFollowing": isFollowing,
        "user_profile": user,
        "whoYouLiked": whoYouLikedPosts,
        "whoYouLikedComments": whoYouLikedComments,
    })


@login_required
def follow(request):
    userfollow = request.POST["userfollow"]
    current_user = request.user
    userfollowData = User.objects.get(username=userfollow)
    f = Follow(user=current_user, user_follower=userfollowData)
    f.save()
    user_id =userfollowData.id
    
    return HttpResponseRedirect(reverse(profile, kwargs={"user_id": user_id}))


@login_required
def unfollow(request):
    userfollow = request.POST["userfollow"]
    current_user = request.user
    userfollowData = User.objects.get(username=userfollow)
    f = Follow.objects.get(user=current_user, user_follower=userfollowData)
    f.delete()
    user_id =userfollowData.id
    
    return HttpResponseRedirect(reverse(profile, kwargs={"user_id": user_id}))


def following(request):
    current_user = User.objects.get(pk=request.user.id)
    followingPeople = Follow.objects.filter(user=current_user)
    allPosts = Post.objects.all().order_by("id").reverse()
    
    followingPosts = []
    
    whoYouLikedPosts = []
    whoYouLikedComments = []
    
    if request.user.is_authenticated:
        # Get posts liked by the user
        post_likes = Like.objects.filter(user=request.user)
        whoYouLikedPosts = [like.post.id for like in post_likes]

        # Get comments liked by the user
        comment_likes = CommentLike.objects.filter(user=request.user)
        whoYouLikedComments = [like.comment.id for like in comment_likes]
    
    for post in allPosts:
        for person in followingPeople:
            if person.user_follower == post.creator:
                followingPosts.append(post)
                
    # Pagination
    paginator = Paginator(followingPosts, 10)
    page_number = request.GET.get("page")
    pagePosts = paginator.get_page(page_number)
    
    return render(request, "network/following.html", {
        "pagePosts": pagePosts,
        "whoYouLiked": whoYouLikedPosts,
        "whoYouLikedComments": whoYouLikedComments,       
    })

   
@login_required    
def edit(request, post_id):
    if request.method == "POST":
        data = json.loads(request.body)
        editPost = Post.objects.get(pk=post_id)
        editPost.content = data["content"]
        editPost.save()
        return JsonResponse({"message": "Change Successful", "data": data["content"]})
        
@login_required
def removeLike(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = request.user
    likes_count = Like.objects.filter(post=post).count()

    try:
        like = Like.objects.get(user=user, post=post)
        like.delete()
        likes_count -= 1  # Decrement the likes_count
        return JsonResponse({"message": "Like removed", "likes_count": likes_count})
    except Like.DoesNotExist:
        return JsonResponse({"message": "Like not found", "likes_count": likes_count}, status=400)


@login_required
def addLike(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = request.user
    likes_count = Like.objects.filter(post=post).count()

    # Check if a like already exists for the user and post
    existing_like = Like.objects.filter(user=user, post=post).first()

    if existing_like:
        return JsonResponse({"message": "Like already exists", "likes_count": likes_count}, status=400)

    # If the like doesn't exist, create a new one
    newLike = Like(user=user, post=post)
    newLike.save()

    likes_count += 1  # Increment the likes_count
    return JsonResponse({"message": "Like added", "likes_count": likes_count})


@login_required
def addComment(request, id):
    current_user = request.user
    postData = Post.objects.get(pk=id)
    message = request.POST["newComment"]
    
    # Collect comment info to store
    newComment = Comment(
        author=current_user,
        post=postData,
        message=message,
        created_at=timezone.now()
    )
    
    # Save the comment
    newComment.save()
    
    return HttpResponseRedirect(reverse("index"))


@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    user = request.user

    # Check if the user has already liked the comment
    if user in comment.likes.all():
        # If already liked, unlike it
        CommentLike.objects.filter(comment=comment, user=user).delete()
    else:
        # Otherwise, add a like
        CommentLike.objects.create(comment=comment, user=user)

    # Get the updated likes count for the comment
    likes_count = comment.likes.count()

    # Prepare the response data
    response_data = {
        # "message": "Comment liked/unliked",
        "likes_count": likes_count,
    }

    return JsonResponse(response_data)


def search(request):
    query = request.GET.get('q')
    
    # Pass the likes to the template
    whoYouLikedPosts = []
    whoYouLikedComments = []
    
    if request.user.is_authenticated:
        # Get posts liked by the user
        post_likes = Like.objects.filter(user=request.user)
        whoYouLikedPosts = [like.post.id for like in post_likes]

        # Get comments liked by the user
        comment_likes = CommentLike.objects.filter(user=request.user)
        whoYouLikedComments = [like.comment.id for like in comment_likes]

    if query:
        # Search for posts with content that contains the query
        posts_with_matching_content = Post.objects.filter(content__icontains=query)
        
        # Search for posts with matching comments
        matching_comments = Comment.objects.filter(message__icontains=query)
        post_ids_with_matching_comments = matching_comments.values_list('post', flat=True)
        posts_with_matching_comments = Post.objects.filter(pk__in=post_ids_with_matching_comments)
        
        # Search for users with usernames that contain the query
        users_with_matching_username = User.objects.filter(username__icontains=query)
        user_posts = Post.objects.filter(creator__in=users_with_matching_username)
        
        # Combine the search results
        posts = (posts_with_matching_content | posts_with_matching_comments | user_posts).distinct()
    else:
        posts = []

    return render(request, "network/search_results.html", {
        "posts": posts,
        "query": query,
        "whoYouLiked": whoYouLikedPosts,
        "whoYouLikedComments": whoYouLikedComments,
    })