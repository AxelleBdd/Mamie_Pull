from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render


def user_login(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        # session creation
        login(request, user)
        return redirect('home')
    else:
        messages.error(request, "Login details invalid")
            
    return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
    return redirect("login")
