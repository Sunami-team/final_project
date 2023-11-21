# tasks.py in one of your Django apps
from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_approval_email(email, course_name):
    send_mail(
        "Course Drop Request Approved",
        f"Your request to drop {course_name} has been approved.",
        "dev.fahima@gmail.com",
        [email],
        fail_silently=False,
    )


@shared_task
def send_rejection_email(email, course_name, rejection_reason):
    send_mail(
        "Course Drop Request Rejected",
        f"Your request to drop {course_name} has been rejected. Reason: {rejection_reason}",
        "dev.fahima@gmail.com",  # Replace with your actual email
        [email],
        fail_silently=False,
    )
