from django import forms

from accounts.models import User


class SighUpForm(forms.Form):
    username = forms.CharField(max_length=50)
    password1 = forms.CharField(widget=forms.PasswordInput(), label='password')
    password2 = forms.CharField(widget=forms.PasswordInput(), label='password confirm')
    full_name = forms.CharField(max_length=100)


    def save(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password1']
        name     = self.cleaned_data['name']
        user = User.objects.create(
            username=username,
            password=password,
            name=name)
        user.set_password(password)
        user.save()


class CommentForm(forms.Form):
    text = forms.CharField()



