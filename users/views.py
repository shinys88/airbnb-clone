from django.shortcuts import render
from django.views import View
from . import forms

# Create your views here.

# class 기반 View
class LoginView(View):

    # get / post
    def get(self, request):

        form = forms.LoginForm()
        return render(request, "users/login.html", {"form":form})
        
    def post(self, request):
        pass


# function 기반 View
def login_view(request):
    if request.method == "GET":
        pass
    elif request.method == "POST":
        pass