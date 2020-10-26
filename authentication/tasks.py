from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.contrib.auth.models import User
from authentication.models import Otp
from authentication.utils import id_generator
from authentication.service import send_email


@shared_task
def post_user(user):
    user_data = User.objects.filter(id=user)
    user_update = user_data.update(is_active=False)
    account_activation_mailer.delay(user)
    return ({'message':'user status udpated'})

@shared_task
def account_activation_mailer(user):
    user_data = User.objects.filter(id=user)
    otp_data = Otp.objects.filter(user=user_data.first(),otp_for="ACTIVATION")

    if otp_data.exists():
        otp_data.delete()

    otp = id_generator()
    otp_save = Otp.objects.create(otp=otp,otp_for="Activation",user=user_data.first())
    trigger_email.delay(user=user_data.first().id,otp=otp)
    return {'message':'Activation Mailer Sent.'}

@shared_task
def trigger_email(user,otp):
    user = User.objects.get(id = user)
    email_data={
      "email":user.email,
      "subject":"ACTIVATE YOUR ACCOUNT",
      "message":"activate your account",
      "username":user.username,
      "otp":otp
    }
    mail_html = "Your OTP password is %s" % email_data["otp"]
    email_content = {
        'message': email_data["message"], 'to_adder': [email_data["email"]],
        'subject': email_data["subject"],
        'mail_html': mail_html,'from_addr': 'subramanian@playtonia.com',
    }
    send_email(email_content)