from django import forms

from .models import Chat


class ChatCreateForm(forms.ModelForm):

    class Meta:
        model = Chat
        fields = ["title", "content", "address", "channel", "uid", "send_to"]


class CreateChatForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)
    address = forms.CharField(widget=forms.HiddenInput)
    channel = forms.CharField(widget=forms.HiddenInput)
    uid = forms.CharField(widget=forms.HiddenInput)
    send_to = forms.CharField(widget=forms.HiddenInput)

    def clean(self):
        send_to = self.cleaned_data.get('send_to')
        channel = self.cleaned_data.get('channel')

        if send_to != channel:
            raise forms.ValidationError("Channel and send to address do not match")
