import json

from core.tests import BranduBaseAPITestCase
from products.models import Product, MainCategory, SubCategory


class BranduBasketAPITestCase(BranduBaseAPITestCase):
    main_category: MainCategory
    sub_category: SubCategory
    product: Product

    def create_basket(self):
        response = self.client.post(
            '/v1/accounts/baskets/1/add',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )
        return response

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.main_category = MainCategory.objects.create(name='테스트 메인 카테고리')
        cls.sub_category = cls.main_category.subcategory_set.create(name='테스트 서브 카테고리')
        cls.product = Product.objects.create(
            name='테스트 상품',
            category=cls.sub_category,
            price=10000,
        )

    def setUp(self):
        super().setUp()

    def test_basket_list_not_exists(self):
        # 인증된 요청의 경우
        response = self.client.get('/v1/accounts/baskets', HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 200)

        baskets = response.json()
        self.assertEqual(baskets['success'], True)
        self.assertIsInstance(baskets['results'], list)
        self.assertEqual(len(baskets['results']), 0)

    def test_basket_create(self):
        response = self.create_basket()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['success'], True)

        # 장바구니 데이터 유무 확인
        response = self.client.get('/v1/accounts/baskets', HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 200)

        baskets = response.json()
        self.assertEqual(baskets['success'], True)
        self.assertIsInstance(baskets['results'], list)
        self.assertEqual(len(baskets['results']), 1)

    def test_basket_create_already_exists(self):
        response = self.create_basket()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['success'], True)

        # 중복 생성한 경우
        response = self.create_basket()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['success'], False)

    def test_basket_destroy(self):
        response = self.create_basket()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['success'], True)

        response = self.client.delete(
            '/v1/accounts/baskets/1',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )

        self.assertEqual(response.status_code, 204)

        # 장바구니 데이터 유무 확인
        response = self.client.get('/v1/accounts/baskets', HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 200)

        baskets = response.json()
        self.assertEqual(baskets['success'], True)
        self.assertIsInstance(baskets['results'], list)
        self.assertEqual(len(baskets['results']), 0)

    def test_basket_purchase_create(self):
        response = self.create_basket()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['success'], True)

        response = self.client.patch(
            '/v1/accounts/baskets/purchase',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            content_type='application/json',
            data=json.dumps([
                {'product': 1, 'amount': 1},
            ]),
        )

        purchase = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(purchase['success'], True)
        self.assertEqual(purchase['results']['message'], '구매가 처리가 완료되었습니다.')

    def test_basket_purchase_create_validation_error(self):
        response = self.create_basket()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['success'], True)

        response = self.client.patch(
            '/v1/accounts/baskets/purchase',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            content_type='application/json',
            data=json.dumps([
                {'product': 5, 'amount': 1},
            ]),
        )

        purchase = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(purchase['success'], False)

    def test_basket_purchase_list(self):
        response = self.create_basket()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['success'], True)

        # 장바구니 구매 리스트 생성
        response = self.client.patch(
            '/v1/accounts/baskets/purchase',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            content_type='application/json',
            data=json.dumps([
                {'product': 1, 'amount': 1},
            ]),
        )
        self.assertEqual(response.status_code, 201)

        response = self.client.get(
            '/v1/accounts/baskets/purchase',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )

        purchase = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(purchase['success'], True)
