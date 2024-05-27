from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from .forms import LoginForm, RegistrationForm
from django.contrib.auth.decorators import login_required
from .models import Room, Message
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from.forms import SignUpForm


User = get_user_model()

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Handle login logic here
            # e.g., authenticate user and log them in
            pass
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


@login_required(login_url='login')
def rooms(request):
    rooms = Room.objects.all()
    return render(request, "rooms.html", {"rooms": rooms})

@login_required(login_url='login')
def room(request, slug):
    try:
        room_instance = Room.objects.filter(slug=slug).first()
        if room_instance is None:
            raise Room.DoesNotExist("Room does not exist with the specified slug.")
        room_name = room_instance.name
        messages = Message.objects.filter(room=room_instance)
        users = User.objects.exclude(username=request.user.username)
        return render(request, "room.html", {"room_name": room_name, "slug": slug, "messages": messages})
    except Room.DoesNotExist:
        # Handle the case where no room exists with the specified slug
        return render(request, "404.html", status=404)
    except Exception as e:
        # Handle any other unexpected errors gracefully
        return render(request, "error.html", {"error_message": str(e)}, status=500)

def signupPage(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


# views.py


User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            return HttpResponseRedirect(reverse('rooms'))  # Redirect to rooms page after successful registration
    else:
        form = SignUpForm()
    return render(request, 'registration/register.html', {'form': form})