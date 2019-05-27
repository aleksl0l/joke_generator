from rest_framework import status

from core.tests.test_factory import TestFactory, RequestMixin


class AuthTestCase(TestFactory, RequestMixin):
    valid_username = 'valid_username'
    valid_password = 'valid_password'
    invalid_password = 'invalid_password'

    def test_create_user_and_login(self):
        response_sighup = self.sighup_user(self.valid_username, self.valid_password)
        self.assertEqual(response_sighup.status_code, status.HTTP_201_CREATED)
        response_login = self.login(self.valid_username, self.valid_password)
        self.assertEqual(response_sighup.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response_login.data)

        response_invalid = self.login(self.valid_username, self.invalid_password)
        self.assertEqual(response_invalid.status_code, status.HTTP_400_BAD_REQUEST)
