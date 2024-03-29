from django import forms

from articles.models import Appeal, Mailing


class AppealForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Ваше имя'
    }))

    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'Email'
    }))

    message = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Сообщение...'
    }))

    class Meta:
        model = Appeal
        fields = ["username", "email", 'message']


class MailForm(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'Email'
    }))

    class Meta:
        model = Mailing
        fields = ["email"]
