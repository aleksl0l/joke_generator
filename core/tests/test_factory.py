from typing import Union

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class TestFactory(APITestCase):
    def setUp(self) -> None:
        self.test_username = 'test_username'
        self.test_password = 'Str0ngPASSword'
        self.user = self.create_user(self.test_username, self.test_password)

    @staticmethod
    def create_user(username: str, password: str) -> User:
        return User.objects.create_user(
            username=username,
            password=password
        )


class RequestMixin:
    @staticmethod
    def get_headers(user: User) -> dict:
        token, created = Token.objects.get_or_create(user=user)
        return {
            'HTTP_AUTHORIZATION': f'Token {token.key}',
        }

    def create_joke(self, payload: dict, user: User) -> Response:
        headers = self.get_headers(user)
        url = reverse('jokes')
        return self.client.post(url, payload, format='json', **headers)

    def get_all_jokes(self, user: User) -> Response:
        headers = self.get_headers(user)
        url = reverse('jokes')
        return self.client.get(url, **headers)

    def detail_joke(self, method: str, joke_id: int, payload: Union[dict, None], user: User) -> Response:
        headers = self.get_headers(user)
        url = reverse('detail_joke', args=(joke_id,))
        method = getattr(self.client, method)
        return method(url, data=payload, format='json', **headers)

    def sighup_user(self, username: str, password: str) -> Response:
        url = reverse('user_sighup')
        payload = {'username': username, 'password': password}
        return self.client.post(url, data=payload, fortmat='json')

    def login(self, username: str, password: str) -> Response:
        url = reverse('user_login')
        payload = {'username': username, 'password': password}
        return self.client.post(url, data=payload, fortmat='json')
