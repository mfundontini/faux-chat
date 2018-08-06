from django.urls import path, re_path

from chat import views

app_name = 'chat'

urlpatterns = [
    path('thread', views.ViewThreads.as_view(), name="thread"),
    re_path(r'message/(?P<uid>[^/]+)$', views.MessageDetailView.as_view(), name="detail"),
    path(r'create', views.CreateChatView.as_view(), name="create"),
]
