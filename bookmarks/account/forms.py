from django import forms


# user login form for the user

class LoginForm(forms.Form):
    # get the user username and password using the django forms
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    