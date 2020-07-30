
from django_otp.util import random_hex
from django_otp.oath import TOTP

import time


class TOTPDevice():

    def __init__(self, *args, **kwargs):

        self.step = kwargs.get('step', 120)
        self.last_t = kwargs.get('last_t', -1)
        self.key = kwargs.get('key', random_hex())
        self.digits = kwargs.get('digits', 6)
        self.verified = kwargs.get('verified', False)

    def __create_topt_obj(self):
        totp = TOTP(str(self.key).encode(), step=self.step, digits=self.digits)
        totp.time = time.time()
        return totp

    def generate_token(self):
        totp = self.__create_topt_obj()
        token = str(totp.token())
        return token

    def verify_token(self, token):
        try:
            token = int(token)
        except ValueError:
            self.verified = False
        else:
            totp = self.__create_topt_obj()

            if ((totp.t() > self.last_t) and
                    (totp.verify(token))):
                self.last_t = totp.t()
                self.verified = True
            else:
                self.verified = False

        return self.verified
