from django.urls import path
from . import views

app_name = "chat"
urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("<slug:room_name>/", views.room, name="room"),
    path("<slug:room_name>/send/", views.send_message, name="send_message"),
    path("<slug:room_name>/messages/", views.get_messages, name="get_messages"),
]
