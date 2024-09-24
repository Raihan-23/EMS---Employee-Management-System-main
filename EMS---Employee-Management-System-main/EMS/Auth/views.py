from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

def login_ems(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
           return render(request, 'login.html', {'error': f"Invalid Credentials"})
    
    return render(request, 'login.html')


def logout_ems(request):
    logout(request)
    return redirect('login')