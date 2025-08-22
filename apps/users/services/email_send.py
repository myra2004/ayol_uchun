from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def send_code(subject, intro_text, phone_number, username, token, template, password=None):
    subject = subject
    to_phone_number = phone_number
    context = {
        'subject': subject,
        'intro_text': intro_text,
        'token': token,
        'password': password,
        'frontend_url': 'myra.uz',
    }
    html_content = render_to_string(template, context)
    email = EmailMessage(subject, html_content, to=[to_phone_number])
    email.content_subtype = 'html'
    email.send()