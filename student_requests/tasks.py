# tasks.py in one of your Django apps
from celery import shared_task
from django.core.mail import send_mail, EmailMessage
from io import BytesIO
from reportlab.pdfgen import canvas


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


@shared_task
def create_and_send_pdf(recipient_email, text):
    # Generate PDF from text using ReportLab
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.drawString(100, 750, text)  # Place the text on PDF
    pdf.save()
    buffer.seek(0)

    # Create an EmailMessage with the PDF as attachment
    email = EmailMessage(
        'Subject: Military Service Request Approval',
        'Body: Please find the attached PDF file.',
        'dev.fahima@gmail.com',  # Replace with your sender email
        [recipient_email],
    )
    email.attach('text_to_pdf.pdf', buffer.getvalue(), 'application/pdf')

    # Send the email
    email.send()