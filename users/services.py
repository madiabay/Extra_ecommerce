import random
import uuid
from rest_framework_simplejwt import tokens
from typing import OrderedDict, Protocol
from django.core.cache import cache

from . import repos, models


class UserServicesInterface(Protocol):

    def create_user(self, data: OrderedDict) -> dict: ...

    def verify_user(self, data: OrderedDict) -> models.CustomUser | None: ...

    def create_token(self, data: OrderedDict) -> dict: ...

    def verify_token(self, data: OrderedDict) -> dict | None: ...


class UserServicesV1:
    user_repos: repos.UserReposInterface = repos.UserReposV1()

    def create_user(self, data: OrderedDict) -> dict:
        code = self._generate_code()
        session_id = self._generate_session_id()
        session = {'code': code, **data}
        cache.set(session_id, session, timeout=300)
        self._send_sms_to_phone_number(data['phone_number'], code)

        return {'session_id': session_id}


    def verify_user(self, data: OrderedDict) -> models.CustomUser | None:
        user_data = cache.get(data['session_id'])

        if not user_data:
            return
        
        if user_data['code'] != data['code']:
            return

        self._send_letter_to_email(user_data['email'])
        return self.user_repos.create_user({
            'email': user_data['email'],
            'phone_number': user_data['phone_number'],
        })
    

    def create_token(self, data: OrderedDict) -> dict:
        user = self.user_repos.get_user(data=data)

        code = self._generate_code()
        session_id = self._generate_session_id()
        cache.set(session_id, {'phone_number': str(user.phone_number), 'code': code}, timeout=300)
        self._send_sms_to_phone_number(user.phone_number, code)

        return {'session_id': session_id}


    
    def verify_token(self, data: OrderedDict) -> dict | None:
        session = cache.get(data['session_id'])
        if not session:
            return
        
        if session['code'] != data['code']:
            return

        user = self.user_repos.get_user(data={'phone_number': session['phone_number']})
        refresh = tokens.RefreshToken.for_user(user=user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    

    @staticmethod
    def _send_letter_to_email(email: str) -> None:
        print(f'send letter to {email}')

    @staticmethod
    def _send_sms_to_phone_number(phone_number: str, code: str) -> None:
        print(f'send sms code {code} to {phone_number}')
    
    @staticmethod
    def _generate_code(length: int = 4) -> str:
        numbers = [str(i) for i in range(10)]
        return ''.join(random.choices(numbers, k=length))
    
    @staticmethod
    def _generate_session_id() -> str:
        return str(uuid.uuid4())