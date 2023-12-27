from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import User


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = User.objects.create_user(first_name=first_name,
                                            last_name=last_name,
                                            email=email,
                                            phone_number=phone_number,
                                            username=username,
                                            password=password)
            user.save()
            messages.success(request, 'Registration successful.')
            return redirect('register')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)

    else:
        form = RegistrationForm()
    errors = form.errors.items()
    context = {
        'form': form,
        'errors': errors
    }
    print(f'context{context}')
    return render(request, 'accounts/register.html', context)


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid login credentials!')
            return redirect('login')

    return render(request, 'accounts/login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You logged out successfully')
    return redirect('login')
