import pytest
import helpers

from rest_framework import status


@pytest.mark.django_db
class UserViewTest:
    code = '3333'

    @pytest.fixture(autouse=True)
    def loaddata(self, load_fixtures):
        load_fixtures('users.json')
    

    @pytest.mark.parametrize('case, code, status_code', (
            ('1', code, status.HTTP_201_CREATED),
            ('2', code, status.HTTP_400_BAD_REQUEST),
            ('3', code, status.HTTP_400_BAD_REQUEST),
            ('4', '1111', status.HTTP_400_BAD_REQUEST),
            ('5', code, status.HTTP_400_BAD_REQUEST),
    ))
    def test_create_user(self, case, code, status_code, api_client, mocker):
        mocker.patch('users.services.UserServicesV1._generate_code', return_value=self.code)

        data = helpers.load_json_data(path=f'users/create_user/{case}')
        response = api_client.post(
            '/api/v1/users/create/',
            format='json',
            data=data,
        )

        data = {**response.data, 'code': code}
        response = api_client.post(
            '/api/v1/users/verify/',
            format='json',
            data=data,
        )

        assert response.status_code == status_code
    

    @pytest.mark.parametrize('case, code, status_code', (
        ('1', code, status.HTTP_200_OK),
        ('1', '1111', status.HTTP_400_BAD_REQUEST),
        ('2', code, status.HTTP_400_BAD_REQUEST),
    ))
    def test_create_token(self, case, code, status_code, api_client, mocker):
        mocker.patch('users.services.UserServicesV1._generate_code', return_value=self.code)

        data = helpers.load_json_data(path=f'users/create_token/{case}')
        response = api_client.post(
            '/api/v1/users/token/',
            format='json',
            data=data
        )

        data = {**response.data, 'code': code}
        response = api_client.post(
            '/api/v1/users/token/verify/',
            format='json',
            data=data
        )

        assert response.status_code == status_code
