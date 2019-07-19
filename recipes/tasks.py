# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import send_mail
from settings.base import EMAIL_HOST_USER
from django.template.loader import render_to_string


@shared_task
def send_html_email(subject, recipient_list, template_name, context):
    send_mail(subject=subject, recipient_list=recipient_list, from_email=EMAIL_HOST_USER, fail_silently=False,
              html_message=render_to_string(template_name=template_name, context=context), message='')
