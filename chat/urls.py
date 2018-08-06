from django.urls import path, re_path

from chat import views

app_name = 'chat'

urlpatterns = [
    path('thread', views.thread, name="thread"),
    re_path(r'message/(?P<uid>[^/]+)$', views.detail, name="detail"),
    path(r'create', views.create, name="create"),
]
