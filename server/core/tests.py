from rest_framework.test import APITestCase, APIClient

from accounts.models import User, Profile


class BranduBaseAPITestCase(APITestCase):
    user: User
    profile: Profile
    token: str
    user_data: dict

    @property
    def access_token(self) -> str:
        if self.token:
            return self.token
        response = self.client.post('/v1/auth/token', self.user_data)
        access_token = response.json()['access_token']
        self.token = access_token
        return access_token

    def setUp(self):
        self.client = APIClient()
        self.user_data: dict = {
            'username': 'test_user',
            'email': 'test@test.com',
            'password': 'password'
        }
        self.token: str = ""
