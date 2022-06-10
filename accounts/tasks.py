from celery import shared_task
from accounts.utils import SendCode


send = SendCode()


@shared_task
def send_sms_code_task(phone_number, code):
    return send.send_sms_code(phone_number, code)


@shared_task
def send_mail_code_task(email, code):
    return send.send_mail_code(email, code)
