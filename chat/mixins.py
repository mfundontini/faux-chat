import json

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string

from connector.consts import MOCK_CHANNELS, CHANNEL
from connector.utils import post_to_feersum
from .models import Chat


class AjaxPostMixin(object):
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if self.request.is_ajax():
            if form.is_valid():
                instance = Chat(**form.cleaned_data)
                instance.save()
                post_to_feersum(MOCK_CHANNELS.get(CHANNEL), instance)
                html = render_to_string(self.partial_template, {"instance": instance}, request)
                serialized_data = json.dumps({"html": html})
                return HttpResponse(serialized_data, content_type="application/json")
            raise Exception
        return render(request, self.template_name, {'form': form, 'chats': Chat.objects.all()})
