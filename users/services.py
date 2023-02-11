from rest_framework_simplejwt import tokens
from typing import OrderedDict, Protocol
from . import models, repos


class UserServicesInterface(Protocol):

    def create_user(self, data: OrderedDict) -> None: ...

    def create_token(self, data: OrderedDict) -> dict: ...


class UserServicesV1:
    user_repos: repos.UserReposInterface = repos.UserReposV1()

    def create_user(self, data: OrderedDict) -> None:
        user = self.user_repos.create_user(data=data)
        
        self._send_letter_to_email(user.email)
    
    @staticmethod
    def _send_letter_to_email(email: str) -> None:
        print(f'send letter to {email}')
    
    def create_token(self, data: OrderedDict) -> dict:
        user = self.user_repos.get_user(data=data)

        refresh = tokens.RefreshToken.for_user(user=user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }