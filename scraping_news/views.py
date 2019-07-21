from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from scraping_news.forms import UserDataForm


def loginView(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid:
            username = request.POST['username']
            password = request.POST['password']
            access = authenticate(username=username, password=password)
            if access is not None:
                if access.is_active:
                    login(request, access)
                    return redirect('/')
                else:
                    return render(request, 'noactive.html')
            else:
                return render(request, 'nouser.html')
    else:
        form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'login.html', context)


@login_required(login_url='/login')
def close(request):
    logout(request)
    return redirect('/')


def newUser(request):
    if request.method=='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'newuser.html', context)


@login_required(login_url='/login')
def changeUserData(request):
    if request.method=='POST':
        form = UserDataForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = UserDataForm(instance=request.user)
    context = {'form': form}
    return render(request, 'changeuserdata.html', context)


@login_required(login_url='/login')
def changeUserPassword(request):
    if request.method=='POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = PasswordChangeForm(request.user)
    context = {'form': form}
    return render(request, 'changeuserpassword.html', context)