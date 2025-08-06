from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string

@login_required
def post_list(request):
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
            {'posts': page_obj, 'page_obj': page_obj}
        )
        return JsonResponse({'html': html, 'has_next': page_obj.has_next(), 'next_page_number': next_page_number})

    return render(request, 'posts/post_list.html', {'posts': page_obj, 'page_obj': page_obj})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
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
            form.save()
            return redirect('post_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/post_form.html', {'form': form, 'post': post})
