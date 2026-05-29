from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings


def send_verification_email(request, user):
    profile = user.userprofile
    token = profile.generate_verification_token()

    current_site = get_current_site(request)
    protocol = 'https' if request.is_secure() else 'http'
    verify_url = f'{protocol}://{current_site.domain}/verify-email/{token}/'

    subject = 'Verify your email address'
    html_message = render_to_string('registration/email_verification.html', {
        'user': user,
        'verify_url': verify_url,
    })
    plain_message = f'Hi {user.username},\n\nPlease verify your email by clicking this link:\n{verify_url}\n\nThank you!'

    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False,
    )
