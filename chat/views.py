import json
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Room, Message


def login_view(request):
    if request.user.is_authenticated:
        return redirect("chat:index")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            next_url = request.GET.get("next", "chat:index")
            return redirect(next_url)
        return render(request, "chat/login.html", {"error": "Invalid credentials"})
    return render(request, "chat/login.html")


def logout_view(request):
    logout(request)
    return redirect("chat:index")


def index(request):
    rooms = Room.objects.all()
    return render(request, "chat/index.html", {"rooms": rooms})


@login_required
def room(request, room_name):
    room, created = Room.objects.get_or_create(name=room_name)
    return render(request, "chat/room.html", {"room": room})


@login_required
@require_POST
def send_message(request, room_name):
    room = get_object_or_404(Room, name=room_name)
    data = json.loads(request.body)
    content = data.get("content", "").strip()
    if content:
        message = Message.objects.create(room=room, user=request.user, content=content)
        return JsonResponse({"status": "ok", "id": message.id})
    return JsonResponse({"status": "error", "error": "Empty message"}, status=400)


@login_required
def get_messages(request, room_name):
    room = get_object_or_404(Room, name=room_name)
    after = request.GET.get("after", 0)
    messages = room.messages.filter(id__gt=after)[:50]
    data = [
        {
            "id": m.id,
            "username": m.user.username,
            "content": m.content,
            "created_at": m.created_at.isoformat(),
        }
        for m in messages
    ]
    return JsonResponse({"messages": data})
