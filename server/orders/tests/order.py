from core.tests import BranduBaseAPITestCase


class BranduAddressAPITestCase(BranduBaseAPITestCase):

    def test_order_retrieve(self):
        # 인증 안된 요청의 경우
        response = self.client.get('/v1/accounts/addresses')
        self.assertEqual(response.status_code, 401)

        # 인증된 요청의 경우
        response = self.client.get('/v1/accounts/addresses', HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data['success'], True)
        self.assertIsInstance(response.data['results'], list)
        self.assertEqual(len(response.data['results']), 0)
