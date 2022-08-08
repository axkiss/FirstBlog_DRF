from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse

from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    email_template_name = 'users_api/email_password_reset.html'
    current_site = get_current_site(instance.request)
    site_name = current_site.name
    context = {
        'site_name': site_name,
        'username': reset_password_token.user.username,
        'reset_password_url': "{}?token={}".format(
            instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
            reset_password_token.key)
    }

    message = render_to_string(email_template_name, context)
    email = EmailMessage(f"Password Reset for {site_name}",
                         message,
                         to=[reset_password_token.user.email])
    email.send()
