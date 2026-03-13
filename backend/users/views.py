from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render


def user_login(request):
    if request.method == "POST":
        u = request.POST.get("username")
        p = request.POST.get("password")

        # authentication check
        user = authenticate(request, username=u, password=p)

        if user is not None:
            # session creation
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Login details invalid")

    return render(request, "users/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")
