from django import forms
from articles.models import Appeal
from phonenumber_field.modelfields import PhoneNumberField


class AppealForm(forms.ModelForm):

    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Ваше имя'
    }))

    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'Email',
    }))

    # numberPhone=PhoneNumberField()

    message = forms.CharField(widget=forms.Textarea(attrs={
        'class': '',
        'placeholder': 'Сообщение...'
    }))

    class Meta:
        model = Appeal
        fields = ["username", "email", 'message']
