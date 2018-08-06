import requests
from uuid import uuid4
from json import dumps, loads

from django.http import Http404, HttpRequest, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect

from .models import Chat
from .forms import ChatCreateForm
from connector.consts import mock_channels


def thread(request):
    chats = Chat.objects.all()
    return render(request, "thread.html", {"chats": chats})


def create(request):
    form = ChatCreateForm()
    context = {
        "form": form
    }

    if request.method == "POST":
        form = ChatCreateForm(request.POST)
        context["form"] = form

        if form.is_valid():
            instance = form.save(commit=False)
            instance.uid = uuid4()
            instance.save()
            return redirect(instance.get_absolute_url())
        else:
            return render(request, "create.html", context)

    return render(request, "create.html", context)


def detail(request, uid):
    instance = get_object_or_404(Chat, uid=uid)
    context = {
        "chat": instance,
    }
    return render(request, "detail.html", context)
