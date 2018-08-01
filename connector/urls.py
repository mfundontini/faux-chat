from django.urls import include, path, re_path

from connector import views

urlpatterns = [
    path(r'^channels/$', views.list_channels),
    re_path(r'^channels/(?P<cid>[^/]+)$', views.get_channel),
    re_path(r'^channels/(?P<cid>[^/]+)/messages/$', views.send_message),
    re_path(r'^chat/(?P<cid>[^/]+)/send$', views.chat_send),   
]