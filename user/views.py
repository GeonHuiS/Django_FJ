from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import LoginForm, RegisterForm


User = get_user_model()


def index(request):
    username = "world"
    if request.user.is_authenticated is True:
        username = request.user.username
    return render(request, "index.html", {"username": username})


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/login")
    else:
        logout(request)
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    # 1. /login로 접근하면 로그인 페이지를 통해 로그인이 되게 해주세요
    # 2. login 할 때 form을 활용해주세요
    msg = "Not Valid Username or Password"
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password")
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                pass
            else:
                if user.check_password(raw_password):
                    login(request, user)
                    return HttpResponseRedirect("/") # login success
                else:
                    pass
    else:
        msg = ""
        form = LoginForm()

    return render(request, "login.html", {"form": form, "msg": msg})


def logout_view(request):
    # 3. /logout url을 입력하면 로그아웃 후 / 경로로 이동시켜주세요
    logout(request)
    return HttpResponseRedirect("/")


def user_list_view(request):

    # 8. user 목록은 로그인 유저만 접근 가능하게 해주세요
    if not request.user.is_authenticated:
        print("Not Login")
        return HttpResponseRedirect("/login")

    # 7. /users 에 user 목록을 출력해주세요
    # 9. user 목록은 pagination이 되게 해주세요
    return render(request, "users.html", {
        "users": Paginator(User.objects.all(), 5).get_page(request.GET.get('page'))
    })
