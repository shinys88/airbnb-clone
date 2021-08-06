from django import forms
from . import models

class LoginForm(forms.Form):

    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
    # password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):

        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                # 1) clean_필드명 함수 error출력 방식
                # raise forms.ValidationError("Password is wrong")
                # 2) clean함수 error출력 방식
                self.add_error("password", forms.ValidationError("Password is wrong"))

                # None field error
                # self.add_error(None, forms.ValidationError("Password is wrong"))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist"))



# 1. Model, Form 분리 방식
class SignUpForm1(forms.Form):

    first_name = forms.CharField(max_length=80)
    last_name = forms.CharField(max_length=80)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError("User already exists with that email")
        except models.User.DoesNotExist:
            return email

    # 순차적으로 벨리데이션을 하기때문에 password 이후에 password1 실행됨.
    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")

        if password != password1:
            raise forms.ValidationError("Password confirmation does not match")

    def save(self):
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        user = models.User.objects.create_user(email, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()




# 2. Model, Form 연결 방식 => forms.ModelForm
class SignUpForm(forms.ModelForm):

    # ModelForm Metadata
    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "email")

        widgets = {
            'first_name': forms.TextInput(attrs={"placeholder":"First Name"}),
            'last_name': forms.TextInput(attrs={"placeholder":"Last Name"}),
            'email': forms.EmailInput(attrs={"placeholder":"Email"}),
        }

    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Password"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Confirm Password"}), label="Confirm Password")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError(
                "That email is already taken", code="existing_user"
            )
        except models.User.DoesNotExist:
            return email
            

    # 순차적으로 벨리데이션을 하기때문에 password 이후에 password1 실행됨.
    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")

        if password != password1:
            raise forms.ValidationError("Password confirmation does not match")

    # ModelForm에는 save메서드가 정의되어 있음.
    def save(self, *args, **kwargs):
        # commit=False  >  Object에 저장하고 DB에는 올리지 않는다.
        user = super().save(commit=False)
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        # username = self.cleaned_data.get("username")
        user.username = email
        # set_password => 암호화
        user.set_password(password)
        user.save()
