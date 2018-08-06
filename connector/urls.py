from django.urls import path, re_path

from connector import views

app_name = 'connector'

urlpatterns = [
    path('channels/', views.list_channels, name="channels"),
    re_path(r'channels/(?P<cid>[^/]+)$', views.get_channel, name="channel"),
    re_path(r'channels/(?P<cid>[^/]+)/messages/$', views.receive_message, name="recieve"),
    re_path(r'chat/(?P<cid>[^/]+)/send$', views.chat_send, name="send"),
]
