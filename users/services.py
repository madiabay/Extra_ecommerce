from typing import OrderedDict, Protocol
from . import models, repos


class UserServicesInterface(Protocol):

    def create_user(self, data: OrderedDict) -> None: ...


class UserServicesV1:
    user_repos: repos.UserReposInterface = repos.UserReposV1()

    def create_user(self, data: OrderedDict) -> None:
        user = self.user_repos.create_user(data=data)
        
        self._send_letter_to_email(user.email)
    
    @staticmethod
    def _send_letter_to_email(email: str) -> None:
        print(f'send letter to {email}')