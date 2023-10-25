from django.shortcuts import render, redirect
from .forms import UserProfileForm, CreateUserForm
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from .models import UserProfile
from dashboard.models import Account
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.utils.encoding import force_str
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.forms import PasswordResetForm
from django.db.models.query_utils import Q
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags


# Create your views here.
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST) 
        if form.is_valid():
            user = form.save()

            # Generate a verification token
            token = default_token_generator.make_token(user)

            # Build email content
            current_site = get_current_site(request)
            protocol = 'https' if request.is_secure() else 'http'
            domain = current_site.domain
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = token

            verification_link = f'{protocol}://{domain}/verify-email/{uid}/{token}/'

            # Customize the email content
            context = {
                'user': user,
                'verification_link': verification_link,
            }
            html_message = render_to_string('verification_email.html', context)
            plain_message = strip_tags(html_message)

            subject = 'Transfer Update | October 2023'
            from_email = None
            to_email = user.email

            # Send the email using EmailMultiAlternatives
            msg = EmailMultiAlternatives(subject, plain_message, from_email, [to_email])
            msg.attach_alternative(html_message, "text/html")
            msg.send()

            messages.success(request, f'Hello {user}, please go to your email {user.email} inbox and click on the\
                            received activation link to confirm and complete the registration. Note: Check your spam folder.')

            return redirect('login')
            
    context = {
        'form': form
    }
    return render(request, 'register.html', context)


# New view for email verification
def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.userprofile.email_verified = True
        user.userprofile.save()

        # Send a welcome email
        if user.userprofile.email_verified:
            subject = 'Welcome to Flitrex'

            # Customize the welcome email content
            context = {'user': user}
            html_message = render_to_string('welcome_email.html', context)
            plain_message = strip_tags(html_message)

            from_email = None
            to_email = [user.email]

            # Send the welcome email using EmailMultiAlternatives
            msg = EmailMultiAlternatives(subject, plain_message, from_email, to_email)
            msg.attach_alternative(html_message, "text/html")
            msg.send()

        messages.success(request, 'Email verification successful. You can now log in.')
    else:
        messages.warning(request, 'Email verification link is invalid.')

    return redirect('login')





def login_view(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = None

            if user is not None and user.userprofile.email_verified:  # Check if email is verified
                authenticated_user = authenticate(request, username=username, password=password)
                if authenticated_user is not None:
                    login(request, authenticated_user)
                    messages.success(request, 'Login successful.')
                    return redirect('index')
                else:
                    messages.error(request, 'Invalid username or password.')
            elif user is not None and not user.userprofile.email_verified:
                messages.warning(request, 'Please verify your email before logging in.')
            else:
                messages.warning(request, 'Invalid username or password.')

    context = {'form': form}
    return render(request, 'login.html', context)



def logout_view(request):
    logout(request)
    messages.success(request, 'Logout successful.')
    return redirect('index')

def user_profile(request):
    profile = UserProfile.objects.get(user=request.user)
    account, created = Account.objects.get_or_create(user_profile=profile)
    context = {
        'profile':profile,
        'account': account,
    }
    return render(request, 'user_profile.html', context)

def update_user_profile(request):
    profile = UserProfile.objects.get(user=request.user)
    account, created = Account.objects.get_or_create(user_profile=profile)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
        else:
            messages.info(request, 'Something went wrong!')
            return redirect('update_user_profile')
    else:
        form = UserProfileForm(instance=profile)
    context = {
        'form':form,
        'profile':profile,
        'account': account,
    }
    return render(request, 'update_user_profile.html', context)


def password_reset_custom(request):
    if request.method == 'POST':
        password_form = PasswordResetForm(request.POST)
        if password_form.is_valid():
            data = password_form.cleaned_data['email']
            user_email = User.objects.filter(Q(email=data))
            if user_email.exists():
                for user in user_email:
                    # Generate a reset token
                    token = default_token_generator.make_token(user)

                    # Build reset URL
                    uid = urlsafe_base64_encode(force_bytes(user.pk))
                    reset_url = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})

                    # Customize the email content
                    subject = 'Password Reset'

                    # Customize the password reset email content
                    context = {
                        'user': user,
                        'protocol': 'https' if request.is_secure() else 'http',  # Determine protocol
                        'domain': request.META['HTTP_HOST'],  # Get domain from request
                        'reset_url': reset_url,
                    }
                    html_message = render_to_string('password_reset_email.html', context)
                    plain_message = strip_tags(html_message)

                    from_email = None
                    to_email = [user.email]

                    # Send the password reset email using EmailMultiAlternatives
                    msg = EmailMultiAlternatives(subject, plain_message, from_email, to_email)
                    msg.attach_alternative(html_message, "text/html")
                    msg.send()

                    return redirect('password_reset_done')

    password_form = PasswordResetForm()
    return render(request, 'password_reset_custom.html', {'password_form': password_form})





