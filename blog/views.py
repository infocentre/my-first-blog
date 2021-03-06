from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comment, Contact
from .form import PostForm, CommentForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


# Create your views here.
def post_list(request):
    if request.method =="POST":
        post = request.POST
        email = post['email']
        fullname = post['fullname']
        image = post['image']
        message = post['message']
        Contact.objects.create(name=fullname, email=email,message=message,image=image)
        return redirect('post_list') #리턴하지 않으면 포스트를 전달하는 단에 머물게됨

    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

    return render(request, 'blog/post_list.html', {'posts':posts})

def post_detail(request, pk):
    #Post.objects.get(pk=pk) 이거 대신
    post = get_object_or_404(Post, pk=pk)
    return render(request,'blog/post_detail.html', {'post':post})

@login_required
def post_new(request):
    if request.method =="POST":
        print(request.FILES)
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit =False)
            post.author = request.user
            # post.published_date = timezone.now() # 바로 퍼블리쉬 하게 만듬
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form':form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method =="POST":
        form = PostForm(request.POST, request.FILES, instance = post )
        if form.is_valid():
            post = form.save(commit = False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail',pk=post.pk)
    #인덴트 조심할 것
    else:
        form = PostForm(instance = post)
    return render(request, 'blog/post_edit.html',{'form':form})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts':posts})

@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)
