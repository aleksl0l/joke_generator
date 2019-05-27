from unittest.mock import patch

from django.urls import reverse
from rest_framework import status

from core.models import Joke
from core.tests.test_factory import TestFactory, RequestMixin


class GenerateJokeTestCase(TestFactory, RequestMixin):

    @patch('core.views.requests.get')
    def test_jokes(self, mock_request):
        mock_request.return_value.json.return_value = 'Joke'
        url = reverse('generate_joke')
        response = self.client.post(url, **self.get_headers(self.user))
        self.assertIn('text', response.data)


class JokesFullFlow(TestFactory, RequestMixin):

    joke_payloads = [
        {'text': 'Joke'},
        {'text': 'Joke1'},
        {'text': 'Joke2'},
    ]

    def test_create_and_get_jokes(self):
        for payload in self.joke_payloads:
            response = self.create_joke(payload, self.user)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        all_jokes_response = self.get_all_jokes(self.user)
        self.assertEqual(all_jokes_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(all_jokes_response.data), len(self.joke_payloads))

    def test_detail_delete_update_get(self):
        response = self.create_joke(self.joke_payloads[0], self.user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        joke_id = response.data.get('id')
        response_detail_get = self.detail_joke('get', joke_id, None, self.user)
        self.assertEqual(response_detail_get.status_code, status.HTTP_200_OK)

        new_text = self.joke_payloads[1]
        response_detail_put = self.detail_joke('put', joke_id, new_text, self.user)
        self.assertEqual(response_detail_put.status_code, status.HTTP_200_OK)

        response_detail_get = self.detail_joke('get', joke_id, None, self.user)
        self.assertEqual(response_detail_get.status_code, status.HTTP_200_OK)
        self.assertEqual(response_detail_get.data.get('text'), new_text.get('text'))

        response_detail_delete = self.detail_joke('delete', joke_id, None, self.user)
        self.assertEqual(response_detail_delete.status_code, status.HTTP_204_NO_CONTENT)

        response_detail_get = self.detail_joke('get', joke_id, None, self.user)
        self.assertEqual(response_detail_get.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_same_joke_different_user(self):
        another_user = self.create_user('another_user', 'another_password')
        self.create_joke(self.joke_payloads[0], self.user)
        create_response = self.create_joke(self.joke_payloads[0], another_user)
        joke_id = create_response.data.get('id')
        self.assertEqual(Joke.objects.count(), 1)

        all_jokes_response_user1 = self.get_all_jokes(self.user)
        all_jokes_response_user2 = self.get_all_jokes(another_user)
        self.assertListEqual(all_jokes_response_user1.data, all_jokes_response_user2.data)

        new_text = self.joke_payloads[1]
        response_detail_put = self.detail_joke('put', joke_id, new_text, self.user)
        self.assertEqual(response_detail_put.status_code, status.HTTP_200_OK)

        all_jokes_response_user1 = self.get_all_jokes(self.user)
        all_jokes_response_user2 = self.get_all_jokes(another_user)
        self.assertEqual(len(all_jokes_response_user1.data), len(all_jokes_response_user2.data))
        id1 = all_jokes_response_user1.data[0].get('id')
        id2 = all_jokes_response_user2.data[0].get('id')
        self.assertNotEqual(id1, id2)
