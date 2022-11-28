from core.tests import BranduBaseAPITestCase


class BranduAddressAPITestCase(BranduBaseAPITestCase):
    def create_address(self, address_data: dict = None):
        if address_data is None:
            address_data = self.address_data

        # 인증된 요청의 경우
        response = self.client.post(
            '/v1/accounts/addresses',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            data=address_data
        )

        return response

    def setUp(self):
        super().setUp()
        self.address_data: dict = {
            'name': '테스트 주소',
            'recipient': '테스터',
            'phone_number': '01012345678',
            'address': '테스트 주소',
            'road_name_address': '테스트 도로명 주소',
            'detail_address': '테스트 빌딩 101호',
            'zip_code': '12345',
        }

    # 사용자 주소 목록 조회 테스트 코드
    def test_address_list_not_exists(self):
        # 인증 안된 요청의 경우
        response = self.client.get('/v1/accounts/addresses')
        self.assertEqual(response.status_code, 401)

        # 인증된 요청의 경우
        response = self.client.get('/v1/accounts/addresses', HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data['success'], True)
        self.assertIsInstance(response.data['results'], list)
        self.assertEqual(len(response.data['results']), 0)

    # 사용자 주소 상세 조회 테스트 코드
    def test_address_retrieve_not_exists(self):
        # 인증 안된 요청의 경우
        response = self.client.get('/v1/accounts/addresses')
        self.assertEqual(response.status_code, 401)

        # 인증된 요청의 경우
        response = self.client.get(
            f'/v1/accounts/addresses/1',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['success'], False)

    # 사용자 주소 데이터 생성 API
    def test_address_create(self):
        # 인증 안된 요청의 경우
        response = self.client.post('/v1/accounts/addresses')
        self.assertEqual(response.status_code, 401)

        response = self.create_address()
        self.assertEqual(response.status_code, 201)

        self.assertEqual(response.data['success'], True)
        self.assertEqual(response.data['results']['name'], self.address_data['name'])
        self.assertEqual(response.data['results']['recipient'], self.address_data['recipient'])
        self.assertEqual(response.data['results']['phone_number'], self.address_data['phone_number'])
        self.assertEqual(response.data['results']['address'], self.address_data['address'])
        self.assertEqual(response.data['results']['road_name_address'], self.address_data['road_name_address'])
        self.assertEqual(response.data['results']['detail_address'], self.address_data['detail_address'])
        self.assertEqual(response.data['results']['zip_code'], self.address_data['zip_code'])

    # 사용자 주소 데이터 생성 API
    def test_address_create_validation_error(self):
        # 인증 안된 요청의 경우
        response = self.client.post('/v1/accounts/addresses')
        self.assertEqual(response.status_code, 401)

        address_data = self.address_data.copy()
        address_data.pop('name')

        response = self.create_address(address_data)
        self.assertEqual(response.status_code, 400)

        self.assertEqual(response.data['success'], False)
        self.assertEqual(response.data['error']['code'], 400)
        self.assertIn('name', response.data['error']['message'])

    # 사용자 주소 데이터 수정 테스트 코드
    def test_address_update(self):
        # 인증 안된 요청의 경우
        response = self.client.post('/v1/accounts/addresses')
        self.assertEqual(response.status_code, 401)

        response = self.create_address()
        self.assertEqual(response.status_code, 201)

        # 사용자 주소 수정 요청
        response = self.client.patch(
            f'/v1/accounts/addresses/{response.data["results"]["id"]}',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            data={'name': 'test2'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['success'], True)
        self.assertEqual(response.data['results']['name'], 'test2')

    # 사용자 주소 데이터 삭제 API
    def test_address_destroy(self):
        # 인증 안된 요청의 경우
        response = self.client.delete('/v1/accounts/addresses')
        self.assertEqual(response.status_code, 401)

        response = self.create_address()
        self.assertEqual(response.status_code, 201)

        # 사용자 주소 삭제 요청
        response = self.client.delete(
            f'/v1/accounts/addresses/{response.data["results"]["id"]}',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
        )

        self.assertEqual(response.status_code, 204)

        # 정상 삭제 확인 테스트
        response = self.client.get('/v1/accounts/addresses', HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data['success'], True)
        self.assertEqual(len(response.data['results']), 0)

    # 사용자 주소 목록 조회 테스트 코드
    def test_address_list(self):
        # 인증 안된 요청의 경우
        response = self.client.get('/v1/accounts/addresses')
        self.assertEqual(response.status_code, 401)

        response = self.create_address()
        self.assertEqual(response.status_code, 201)

        # 인증된 요청의 경우
        response = self.client.get('/v1/accounts/addresses', HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data['success'], True)
        self.assertEqual(len(response.data['results']), 1)

    # 사용자 주소 상세 조회 테스트 코드
    def test_address_retrieve(self):
        # 인증 안된 요청의 경우
        response = self.client.get('/v1/accounts/addresses')
        self.assertEqual(response.status_code, 401)

        response = self.create_address()
        self.assertEqual(response.status_code, 201)

        # 인증된 요청의 경우
        response = self.client.get(
            f'/v1/accounts/addresses/{response.data["results"]["id"]}',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
        )
        self.assertEqual(response.data['success'], True)
        self.assertEqual(response.data['results']['name'], self.address_data['name'])
