from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Tag, Comment
from .forms import PostForm, CommentForm
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string
from users.models import User

@login_required
def post_list(request, tag_name=None):
    if tag_name:
        tag = get_object_or_404(Tag, name=tag_name)
        posts = Post.objects.filter(tags=tag).order_by('-created_at')
    else:
        posts = Post.objects.all().order_by('-created_at')

    paginator = Paginator(posts, 5)  # 한 페이지에 5개씩 표시
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if page_obj.has_next():
            next_page_number = page_obj.next_page_number()
        else:
            next_page_number = None
        html = render_to_string(
            'posts/_post_list.html',
            {'posts': page_obj, 'page_obj': page_obj, 'comment_form': CommentForm()}
        )
        return JsonResponse({'html': html, 'has_next': page_obj.has_next(), 'next_page_number': next_page_number})

    return render(request, 'posts/post_list.html', {'posts': page_obj, 'page_obj': page_obj, 'tag': tag_name, 'comment_form': CommentForm()})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            tag_names = form.cleaned_data['tags'].split(',')
            for tag_name in tag_names:
                tag_name = tag_name.strip()
                if tag_name:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    post.tags.add(tag)

            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'posts/post_form.html', {'form': form})

@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return redirect('post_list')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            post.tags.clear()
            tag_names = form.cleaned_data['tags'].split(',')
            for tag_name in tag_names:
                tag_name = tag_name.strip()
                if tag_name:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    post.tags.add(tag)

            return redirect('post_list')
    else:
        form = PostForm(instance=post, initial={'tags': ', '.join([tag.name for tag in post.tags.all()])})
    return render(request, 'posts/post_form.html', {'form': form, 'post': post})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return redirect('post_list')

    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'posts/post_confirm_delete.html', {'post': post})

@login_required
def toggle_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    if user in post.likes.all():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True
    return JsonResponse({'liked': liked, 'likes_count': post.likes.count()})

@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_list')
    return redirect('post_list')

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author != request.user:
        return redirect('post_list')
    
    if request.method == 'POST':
        comment.delete()
        return redirect('post_list')
    return redirect('post_list')

def search(request):
    query = request.GET.get('q')
    if query:
        users = User.objects.filter(username__icontains=query)
        tags = Tag.objects.filter(name__icontains=query)
    else:
        users = User.objects.none()
        tags = Tag.objects.none()
    
    context = {
        'query': query,
        'users': users,
        'tags': tags,
    }
    return render(request, 'search_results.html', context)
