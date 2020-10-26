from django.core.mail import EmailMultiAlternatives


def send_email(message):
    from_addr = message.get('from_addr','subramanian@playtonia.com')
    msg_html = message.get('mail_html')
    carbon_copy = message.get('cc', [])

    mail = EmailMultiAlternatives(
        subject=message['subject'], body=message['message'],
        from_email=from_addr, to=message['to_adder'],
        cc=carbon_copy,
    )
    mail.attach_alternative(msg_html, "text/html")
    mail.send()