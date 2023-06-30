from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail


from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)

        print('Вызов метода save')

        send_mail(
            subject='Добро пожаловать на наш портал!',
            message=f'{user.username}, вы успешно зарегестрировались!',
            from_email=None,
            recipient_list=[user.email]
        )

        return user