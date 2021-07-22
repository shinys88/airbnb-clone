from django import forms
from . import models

class LoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    # clean_ + field명
    def clean_email(self):
        # clean_함수는 return 값으로 view로 넘겨줌.
        # return "asdsadas"
        print("clean email")
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(username=email)
            return email
        except models.User.DoesNotExist:
            raise forms.ValidationError("User does not exist")


    def clean_password(self):

        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        try:
            user = models.User.objects.get(username=email)
            if user.check_password(password):
                return email
            else:
                raise forms.ValidationError("Password is wrong")

        except models.User.DoesNotExist:
            pass

        print("clean ps")
