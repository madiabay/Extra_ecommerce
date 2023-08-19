import logging
import random
import uuid
from rest_framework_simplejwt import tokens
from typing import OrderedDict, Protocol
from django.core.cache import cache
from django.core.mail import send_mail
from templated_email import send_templated_mail
from django.conf import settings

from . import repos, models

from rest_framework.exceptions import ValidationError


logger = logging.getLogger(__name__)

class UserServicesInterface(Protocol):

    def create_user(self, data: OrderedDict) -> dict: ...

    def verify_user(self, data: OrderedDict) -> models.CustomUser | None: ...

    def create_token(self, data: OrderedDict) -> dict: ...

    def verify_token(self, data: OrderedDict) -> dict | None: ...


class UserServicesV1:
    user_repos: repos.UserReposInterface = repos.UserReposV1()

    def create_user(self, data: OrderedDict) -> dict:
        return self._verify_phone_number(data=data)


    def verify_user(self, data: OrderedDict) -> models.CustomUser | None:
        user_data = cache.get(data['session_id'])

        if not user_data:
            raise ValidationError
        
        if user_data['code'] != data['code']:
            raise ValidationError

        self._send_letter_to_email(user=user_data)
        return self.user_repos.create_user({
            'email': user_data['email'],
            'phone_number': user_data['phone_number'],
        })
    

    def create_token(self, data: OrderedDict) -> dict:
        return self._verify_phone_number(data=data, is_exist=True)

    
    def verify_token(self, data: OrderedDict) -> dict | None:
        session = cache.get(data['session_id'])
        if not session:
            raise ValidationError
        
        if session['code'] != data['code']:
            raise ValidationError

        user = self.user_repos.get_user(data={'phone_number': session['phone_number']})
        refresh = tokens.RefreshToken.for_user(user=user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    

    @staticmethod
    def _send_letter_to_email(user: models.CustomUser) -> None:
        send_templated_mail(
            template_name='welcome',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user['email']],
            context={
                'phone_number': user['phone_number'],
                'email': user['email'],
            }
        )
    

    def _verify_phone_number(self, data: OrderedDict, is_exist: bool = False) -> str:
        if is_exist:
            self.user_repos.get_user(data=data)

        code = self._generate_code()
        session_id = self._generate_session_id()
        cache.set(session_id, {'code': code, **data}, timeout=300)
        self._send_sms_to_phone_number(data['phone_number'], code)
        
        return {'session_id': session_id}

    
    @staticmethod
    def _send_sms_to_phone_number(phone_number: str, code: str) -> None:
        logger.info(f'send sms code {code} to {phone_number}')
    
    @staticmethod
    def _generate_code(length: int = 4) -> str:
        numbers = [str(i) for i in range(10)]
        return ''.join(random.choices(numbers, k=length))
    
    @staticmethod
    def _generate_session_id() -> str:
        return str(uuid.uuid4())