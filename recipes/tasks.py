# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import send_mail
from HipoProject.settings import EMAIL_HOST_USER
from django.template.loader import render_to_string


@shared_task
def send_email_wrapper(subject, recipient_list, context):
    send_mail(subject=subject, recipient_list=recipient_list, from_email=EMAIL_HOST_USER, fail_silently=False,
              message='Test Message', html_message=render_to_string(template_name='emails/email.html', context=context))
