from celery import shared_task
from django.core.mail import send_mail
from courses.models import Faculty


@shared_task
def send_email_task(subject, message, from_email, recipient_list):
    send_mail(subject, message, from_email, recipient_list)

@shared_task
def alaki():
    q =Faculty.objects.create(name='zagoori')
    q.save()
    print('inam az un')