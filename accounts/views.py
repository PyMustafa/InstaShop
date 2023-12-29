from django.contrib import messages, auth
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import RegistrationForm

User = get_user_model()


def send_verification_email(request, user):
    current_site = get_current_site(request)
    mail_subject = "Activate your account!"

    message = render_to_string('accounts/account_verification_email.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    }, request)
    to_email = user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.content_subtype = 'html'
    send_email.send()


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

            send_verification_email(request, user)

            return redirect(f'/account/login/?command=verification&email={user.email}')
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


def verify_email_confirm(request, uidb64, token):
    try:
        user_id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=user_id)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.email_is_verified = True
        user.save()
        messages.success(request, 'Your email has been verified.')
    else:
        messages.warning(request, 'The link is invalid.')
    return redirect('login')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = auth.authenticate(email=email, password=password)
        if user is not None:
            if user.email_is_verified:
                auth.login(request, user)
                return redirect('home')
            else:
                send_verification_email(request, user)
                return redirect(f'/account/login/?command=verification&email={user.email}')
        else:
            messages.error(request, 'Invalid login credentials!')
            return redirect('login')

    return render(request, 'accounts/login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You logged out successfully')
    return redirect('home')


def forget_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            # send reset password email
            current_site = get_current_site(request)
            mail_subject = "Reset Password Request"
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            }, request)
            to_email = user.email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.content_subtype = 'html'
            send_email.send()
            messages.success(request, 'Password reset email has been sent to your email address.')
            redirect('login')

        else:
            messages.error(request, 'Sorry, we could not find your account.')

    return render(request, 'accounts/forget_password.html')


def reset_password_validate(request, uidb64, token):
    uid = force_str(urlsafe_base64_decode(uidb64))
    try:
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'You can reset your password now')
        return redirect('reset-password')
    else:
        messages.error(request, 'The link is invalid.')
        return redirect('login')


def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm-password']
        user = User.objects.filter(pk=request.session.get('uid')).first()  # if not found => user = None
        # user = User.objects.get(pk=request.session.get('uid'))  # if not found => Raise DoesNotExist error

        if not user:
            messages.error(request, 'Expired Link, try again.')
            return redirect('login')

        if password == confirm_password:
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset Successfully.')
        else:
            messages.error(request, 'Password and confirm password does not match!')

    return render(request, 'accounts/reset_password.html')
