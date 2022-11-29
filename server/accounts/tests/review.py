from accounts.models import User, Profile
from core.tests import BranduBaseAPITestCase
from orders.models import Order, OrderProduct
from products.models import MainCategory, Product, SubCategory


class BranduReviewAPITestCase(BranduBaseAPITestCase):
    main_category: MainCategory
    sub_category: SubCategory
    product: Product

    def create_review(self, review_data: dict = None):
        if review_data is None:
            review_data = self.review_data

        # 인증된 요청의 경우
        response = self.client.post(
            '/v1/accounts/reviews',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            data=review_data
        )

        return response

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.main_category = MainCategory.objects.create(name='테스트 메인 카테고리')
        cls.sub_category = cls.main_category.subcategory_set.create(name='테스트 서브 카테고리')
        cls.user = User.objects.create_user(username='review_test_user', email='test@test.com', password='password')
        cls.profile = Profile.objects.create(user=cls.user)
        cls.order = Order.objects.create(
            profile=cls.profile,
            name='테스트 주문',
            price=50000,
            method='card',
        )
        cls.product = Product.objects.create(
            name='테스트 상품',
            category=cls.sub_category,
            price=10000,
        )
        cls.order_product = OrderProduct.objects.create(
            order=cls.order,
            product=cls.product,
            count=1,
        )

    def setUp(self):
        super().setUp()
        self.review_data: dict = {
            'order_product': self.order_product.id,
            'comment': '테스트 리뷰',
            'star': 5,
        }

    # 사용자 리뷰 목록 조회 테스트 코드
    def test_review_list_not_exists(self):
        # 인증 안된 요청의 경우
        response = self.client.get('/v1/accounts/reviews')
        self.assertEqual(response.status_code, 401)

        # 인증된 요청의 경우
        response = self.client.get('/v1/accounts/reviews', HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['success'], True)
        self.assertIsInstance(response.data['results'], list)
        self.assertEqual(len(response.data['results']), 0)

    # 사용자 리뷰 작성 가능 목록 조회 테스트 코드
    def test_review_writable_list(self):
        # 인증 안된 요청의 경우
        response = self.client.get('/v1/accounts/reviews/writable')
        self.assertEqual(response.status_code, 401)

        # 인증된 요청의 경우
        response = self.client.get('/v1/accounts/reviews/writable', HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 200)

    # 사용자 리뷰 생성 테스트 코드
    def test_review_create(self):
        # 인증 안된 요청의 경우
        response = self.client.post('/v1/accounts/reviews', data=self.review_data)
        self.assertEqual(response.status_code, 401)

        # 인증된 요청의 경우
        response = self.create_review()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['success'], True)
        self.assertEqual(response.data['results']['order_product'], self.review_data['order_product'])
        self.assertEqual(response.data['results']['comment'], self.review_data['comment'])
        self.assertEqual(response.data['results']['star'], self.review_data['star'])
