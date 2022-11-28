from accounts.models import User, Profile
from core.tests import BranduBaseAPITestCase


class BranduFollowAPITestCase(BranduBaseAPITestCase):
    def create_follow(self):
        response = self.client.post(
            f'/v1/accounts/follows/{self.profile.id}/follow',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )
        return response

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = User.objects.create_user(username='follow_test_user', email='test@test.com', password='password')
        cls.profile = Profile.objects.create(user=cls.user)

    def test_follow_list(self):
        response = self.client.get('/v1/accounts/follows')
        self.assertEqual(response.status_code, 401)

        response = self.client.get('/v1/accounts/follows', HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data['success'], True)
        self.assertIsInstance(response.data['results'], dict)
        self.assertEqual(response.data['results']['follower'], [])
        self.assertEqual(response.data['results']['following'], [])

    def test_follow_create(self):
        response = self.create_follow()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['success'], True)
        self.assertEqual(response.data['results']['message'], '팔로우 되었습니다.')

        response = self.client.get('/v1/accounts/follows', HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.assertEqual(response.data['success'], True)
        self.assertIsInstance(response.data['results'], dict)
        self.assertNotEqual(response.data['results']['follower'], [])
        self.assertEqual(response.data['results']['following'], [])

    def test_follow_create_twice(self):
        response = self.create_follow()
        self.assertEqual(response.status_code, 201)

        # 이미 팔로우한 경우
        response = self.create_follow()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['success'], False)
        self.assertEqual(response.data['error']['message'], '해당 관계가 이미 존재하기때문에 추가할 수 없습니다.')

    def test_follow_destroy_before_create(self):
        response = self.client.delete(
            f'/v1/accounts/follows/{self.profile.id}/follow',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['success'], False)
        self.assertEqual(response.data['error']['message'], '해당 관계가 존재하지 않기 때문에 삭제할 수 없습니다.')

    def test_follow_create_and_destroy(self):
        response = self.create_follow()
        self.assertEqual(response.status_code, 201)

        response = self.client.delete(
            f'/v1/accounts/follows/{self.profile.id}/follow',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
        )

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data['success'], True)
        self.assertEqual(response.data['results']['message'], '팔로우가 해제되었습니다.')

    def test_follow_list_without_authenticate(self):
        response = self.client.get(f'/v1/accounts/follows/{self.profile.id}')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data['success'], True)
        self.assertIsInstance(response.data['results'], dict)
        self.assertEqual(response.data['results']['follower'], [])
        self.assertEqual(response.data['results']['following'], [])
