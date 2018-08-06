import requests
from uuid import uuid4
from json import dumps, loads

from django.http import Http404, HttpRequest, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect

from .models import Chat
from .forms import ChatCreateForm
from connector.consts import USER, CHANNEL, MOCK_CHANNELS


def thread(request):
    chats = Chat.objects.all()
    return render(request, "thread.html", {"chats": chats})


def create(request):
    form = ChatCreateForm()
    context = {
        "form": form
    }
    channel = MOCK_CHANNELS.get(CHANNEL)

    if request.method == "POST":
        form = ChatCreateForm(request.POST)
        context["form"] = form

        if form.is_valid():
            instance = form.save(commit=False)
            instance.uid = str(uuid4())
            instance.channel = CHANNEL
            instance.address = USER
            instance.send_to = CHANNEL
            instance.save()

            # try:
            res = requests.post(
                channel["mo_url"],
                json={
                    'channel_data': {
                        'session_event': 'resume'
                    },
                    'from': instance.address,
                    'channel_id': CHANNEL,
                    'timestamp': str(instance.timestamp),
                    'content': instance.content,
                    'to': CHANNEL,
                    'reply_to': None,
                    'message_id': instance.uid
                }
            )
            # except
            # finally:
            print(res.status_code, res.reason)

            return redirect(instance.get_absolute_url())
        else:
            return render(request, "create.html", context)

    return render(request, "create.html", context)


def detail(request, uid):
    instance = get_object_or_404(Chat, uid=uid)
    return render(request, "detail.html", {"chat": instance})
