from django.urls import path, re_path

from chat import views

app_name = 'chat'

urlpatterns = [
    path('thread', views.thread),
    re_path(r'message/(?P<cid>[^/]+)$', views.detail),
    path(r'create', views.create),
]
