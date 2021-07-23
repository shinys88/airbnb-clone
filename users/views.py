from django.shortcuts import render, redirect, reverse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from . import forms

# Create your views here.

# class 기반 View
class LoginView(View):

    # get / post
    def get(self, request):
        form = forms.LoginForm(initial={"email":"sss@sss.sss"})
        return render(request, "users/login.html", {"form":form})
        
    def post(self, request):
        form = forms.LoginForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            print(form.cleaned_data)
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse("core:home"))


        return render(request, "users/login.html", {"form":form})




# function 기반 View
def login_view(request):
    if request.method == "GET":
        pass
    elif request.method == "POST":
        pass

from django.contrib.auth import logout
def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))



# class기반 FormView
from django.views.generic import FormView
from django.urls import reverse_lazy
class LoginFormView(FormView):

    # UserView => username과 password를 사용하야함. email 사용 불가능하여 FormView 추천

    template_name = "users/login.html"
    form_class = forms.LoginForm
      # reverse_lazy : reverse와 같은데 자동으로 호출하지 않음 / View가 필요로 할때 호출
    success_url = reverse_lazy("core:home")
    initial = {
        "email": "sys0130@naver.com"
    }

    # FormView 검증 방식.
    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")
    initial = {
        "first_name":"YS",
        "last_name":"Shin",
        "email":"sys0130@naver.com",
    }

    def form_valid(self, form):
        form.save()

        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)

        return super().form_valid(form)