import requests
from uuid import uuid4
from json import dumps, loads

from django.views.generic import ListView, DetailView, View
from django.shortcuts import render, get_object_or_404, redirect

from .models import Chat
from .forms import CreateChatForm
from connector.consts import USER, MOCK_CHANNELS, CHANNEL
from connector.utils import post_to_feersum


class ViewThreads(ListView):
    model = Chat
    context_object_name = "chats"
    template_name = "thread.html"


class CreateChatView(View):
    form_class = CreateChatForm
    chats = Chat.objects.all()

    initial = {
        "address": USER,
        "channel": CHANNEL,
        "send_to": CHANNEL,
        "uid": str(uuid4())
    }
    template_name = 'create.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form, 'chats': self.chats})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            instance = Chat(**form.cleaned_data)
            instance.save()
            post_to_feersum(MOCK_CHANNELS.get(CHANNEL), instance)
            return redirect(instance.get_absolute_url())

        return render(request, self.template_name, {'form': form, 'chats': self.chats})


class MessageDetailView(DetailView):
    model = Chat
    pk_url_kwarg = "uid"
    context_object_name = "chat"
    template_name = "detail.html"
