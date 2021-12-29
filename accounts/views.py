from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect


from .forms import UserCreationForm


def signup(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        login(request, user)
        return redirect('chat:index')
    return render(request, 'registration/signup.html', {'form': form})

