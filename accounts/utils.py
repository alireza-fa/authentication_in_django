from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from kavenegar import *

from A import local_settings


class SendCode:
    API_KEY = local_settings.KAVE_API_KEY
    SENDER = local_settings.KAVE_SENDER

    def send(self, receiver, message):
        try:
            api = KavenegarAPI(self.API_KEY)
            params = {
                'sender': self.SENDER,
                'receptor': receiver,
                'message': message,
            }
            response = api.sms_send(params)
            print(response)
        except APIException as e:
            print(e)
        except HTTPException as e:
            print(e)

    def send_sms_code(self, phone_number, code):
        self.send(receiver=phone_number, message=code)
        return code

    @staticmethod
    def send_mail_code(email, code):
        return send_mail(_('Otp Code'), code, 'support@alirezafaizi.ir', [email])
