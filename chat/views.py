import requests
from uuid import uuid4
from json import dumps, loads

from django.views.generic import ListView, DetailView, View
from django.shortcuts import render, get_object_or_404, redirect

from .models import Chat
from .forms import CreateChatForm
from .mixins import AjaxPostMixin
from connector.consts import USER, MOCK_CHANNELS, CHANNEL
from connector.utils import post_to_feersum


class ViewThreads(ListView):
    model = Chat
    context_object_name = "chats"
    template_name = "thread.html"


class CreateChatView(AjaxPostMixin, View):
    form_class = CreateChatForm
    partial_template = "create_partial.html"

    initial = {
        "address": USER,
        "channel": CHANNEL,
        "send_to": CHANNEL,
        "uid": str(uuid4())
    }
    template_name = 'create.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form, 'chats': Chat.objects.all()})


class MessageDetailView(DetailView):
    model = Chat
    pk_url_kwarg = "uid"
    context_object_name = "chat"
    template_name = "detail.html"
