from django.shortcuts import render, redirect
from .forms import SignupForm
from .models import User

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')  # 회원가입 성공 시 로그인 페이지로 이동
    else:
        form = SignupForm()
    return render(request, 'users/signup.html', {'form': form})

def find_username(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            username = user.username
        except User.DoesNotExist:
            username = None
        return render(request, 'users/find_username_result.html', {'username': username})
    return render(request, 'users/find_username_form.html')
