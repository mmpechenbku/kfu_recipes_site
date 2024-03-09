from django.shortcuts import render
from django.contrib.auth import get_user_model
from web.forms import RegistrationForm

User = get_user_model()

def home_view(request):
    return render(request, 'web/home.html')

def registration_view(request):
    form = RegistrationForm()
    is_success = False
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"]
            )
            user.set_password(form.cleaned_data["password"])
            user.save()
            is_success = True
    return render(request, "web/registration.html", {
        'form': form,
        'is_success': is_success,
    })