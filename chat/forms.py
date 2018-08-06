from django import forms

from .models import Chat


class ChatCreateForm(forms.ModelForm):

    class Meta:
        model = Chat
        fields = ["title", "content", "address", "channel", "uid", "send_to"]
