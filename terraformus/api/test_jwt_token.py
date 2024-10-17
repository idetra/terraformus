from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from terraformus.core.models import Solution
import uuid


class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.username = 'admin'
        self.password = 'admin'
        User = get_user_model()
        self.user = User.objects.create_user(username=self.username, password=self.password)

        # Create a Solution object with the required UUID and fields
        self.solution_uuid = uuid.UUID('b4063f54-7fff-44e8-8a7a-aabd2bed7d3c')
        self.solution = Solution.objects.create(
            uuid=self.solution_uuid,
            user=self.user,
            title='Test Solution',
            subtitle='Test Subtitle',
            goal='Test Goal',
            update='Test Update',
            upgrade='Test Upgrade',
            scale_up='Test Scale Up',
            # Add other fields with default values or necessary sample data as needed
        )

    def test_token_obtain(self):
        url = '/api/v1/token/'
        response = self.client.post(url, data={'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, 200, response.content)
        tokens = response.json()
        self.assertIn('access', tokens)
        self.assertIn('refresh', tokens)
        self.access_token, self.refresh_token = tokens['access'], tokens['refresh']
        print('Access Token:', self.access_token)
        print('Refresh Token:', self.refresh_token)

    def test_token_refresh(self):
        self.test_token_obtain()
        url = '/api/v1/token/refresh/'
        response = self.client.post(url, data={'refresh': self.refresh_token})
        self.assertEqual(response.status_code, 200, response.content)
        response_json = response.json()
        new_access_token = response_json.get('access')
        self.assertIsNotNone(new_access_token)
        self.new_access_token = new_access_token
        print('New Access Token:', self.new_access_token)

    def test_protected_endpoint(self):
        self.test_token_refresh()
        print('Testing protected endpoint with Access Token:', self.new_access_token)
        url = f'/api/v1/solutions/{self.solution_uuid}'
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.new_access_token)
        response = self.client.get(url)
        print('Response Status Code:', response.status_code)
        print('Response Content:', response.content)
        self.assertEqual(response.status_code, 200, response.content)
        response_json = response.json()

        # Check for specific keys in the response
        expected_keys = {
            'uuid', 'title', 'subtitle', 'goal', 'update', 'upgrade', 'scale_up',
            'created_at', 'edited_at', 'derives_from', 'depends_on'
        }
        for key in expected_keys:
            self.assertIn(key, response_json)

        print('Protected Endpoint Response:', response_json)
