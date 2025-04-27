from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

class PhoneNumberAuthBackend(BaseBackend):
    def authenticate(self, request, phone_number=None, verification_code=None):
        User = get_user_model()
        try:
            user = User.objects.get(phone_number=phone_number)
            if request.session.get('verification_code') == verification_code:
                return user
        except User.DoesNotExist:
            return None
        return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:

            return None