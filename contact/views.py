from django.shortcuts import render, redirect
from django.contrib import messages
from . forms import ContactForm

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

# Create your views here.
# Create your views here!!!
def contact(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            message = form.cleaned_data.get('message')
            html = render_to_string('contactmessage.html', {
                'name': name,
                'email': email,
                'message': message,
            })
            send_mail('Contact Us', html, settings.DEFAULT_FROM_EMAIL, ['madukasblog@gmail.com'], fail_silently=False, html_message=html)
            messages.success(request, "Thank you for reaching us, we'll get back to you shortly.")
            return redirect('contact')
        else:
            messages.info(request, "Something went wrong, please try again.")

    else:
        form = ContactForm()
    context = {
        'form': form,
    }
    return render(request, 'contact.html', context)


