from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint, Deferrable

from core.exceptions.product import RelationAlreadyExistException, RelationDoesNotExistException
from core.exceptions.profile import ProfileNotAllowException, ProfileNotExistException
from core.mixins import BaseModel


class User(AbstractUser):
    pass


class Platform(BaseModel):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    platform = models.CharField(max_length=10)
    platform_id = models.CharField(max_length=100)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['platform', 'platform_id'], name='unique_platform_id',
                             deferrable=Deferrable.DEFERRED),
        ]


class Profile(BaseModel):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE)
    backdrop_image = models.ImageField(upload_to='profile/%Y/%m/%d', null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile/%Y/%m/%d', null=True, blank=True)
    nickname = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=10, null=True)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=15, null=True)
    birth = models.DateField(null=True)
    social_link = models.CharField(max_length=30, null=True)
    description = models.TextField(null=True)
    point = models.IntegerField(default=0)
    wish = models.ManyToManyField('products.Product', through='accounts.WishList',
                                  through_fields=('profile', 'product'), related_name='+')
    basket = models.ManyToManyField('products.Product', through='accounts.Basket',
                                    through_fields=('profile', 'product'), related_name='+')
    scrapped = models.ManyToManyField('communities.Post', related_name='+')

    def follow(self, profile):
        if self.id == profile.id:
            raise ProfileNotAllowException()
        if Following.objects.filter(follower=profile, following=self).exists():
            raise RelationAlreadyExistException()
        Following.objects.create(following=self, follower=profile)

    def unfollow(self, profile):
        if self.id == profile.id:
            raise ProfileNotAllowException()
        if Following.objects.filter(follower=profile, following=self).exists():
            Following.objects.get(follower=profile, following=self).delete()
        raise RelationDoesNotExistException()

    @classmethod
    def get_profile_or_exception(cls, profile_id: int):
        if cls.objects.filter(id=profile_id).exists():
            return cls.objects.get(id=profile_id)
        raise ProfileNotExistException()

    @property
    def favorites(self):
        return self.wish.all()

    @property
    def buckets(self):
        return self.basket.all()


class Address(BaseModel):
    profile = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    recipient = models.CharField(max_length=30)
    address = models.CharField(max_length=200)
    road_name_address = models.CharField(max_length=200)
    detail_address = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=5)
    phone_number = models.CharField(max_length=15)
    memo = models.TextField(null=True)
    is_main = models.BooleanField(default=False)

    def set_main(self) -> None:
        addresses = Address.objects.filter(profile=self.profile)
        addresses.update(is_main=False)
        self.is_main = True
        self.save()


class Point(BaseModel):
    profile = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, related_name='points')
    memo = models.CharField(max_length=200)
    point = models.IntegerField()
    is_use = models.BooleanField(default=False)

    @classmethod
    def create(cls, profile: Profile, memo: str, point: int):
        profile.point += point
        profile.save()
        return cls.objects.create(
            profile=profile,
            memo=memo,
            point=point
        )

    @classmethod
    def use(cls, profile: Profile, memo: str, point: int):
        profile.point -= point
        profile.save()
        return cls.objects.create(
            profile=profile,
            memo=memo,
            point=point,
            is_use=True
        )


class WishList(models.Model):
    profile = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, related_name='+')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='+')

    @staticmethod
    def add(profile, product):
        """ WishList에 새로운 상품을 추가하는 함수 """
        if profile.wish.filter(id=product.id).exists():
            raise RelationAlreadyExistException()
        profile.wish.add(product)

    @staticmethod
    def remove(profile, product):
        """ WishList에 있는 상품을 제거하는 함수 """
        if profile.wish.filter(id=product.id).exists():
            raise RelationDoesNotExistException()
        profile.wish.remove(product)


class Basket(models.Model):
    profile = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, related_name='+')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='+')
    amount = models.IntegerField(default=1)
    is_purchase = models.BooleanField(default=False)

    @staticmethod
    def add(profile, product):
        """ Basket에 새로운 상품을 추가하는 함수 """
        if profile.basket.filter(id=product.id).exists():
            raise RelationAlreadyExistException()
        profile.basket.add(product)

    @staticmethod
    def remove(profile, product):
        """ Basket에 있는 상품을 제거하는 함수 """
        if not profile.basket.filter(id=product.id).exists():
            raise RelationDoesNotExistException()
        profile.basket.remove(product)

    def purchase(self, amount: int):
        """ Basket에 담긴 상품을 구매하는 함수 """
        self.amount = amount
        self.is_purchase = True
        self.save()


class Notify(BaseModel):
    profile = models.OneToOneField('accounts.Profile', on_delete=models.CASCADE)
    is_store = models.BooleanField(default=False)
    is_community = models.BooleanField(default=False)
    is_event = models.BooleanField(default=False)


class Following(models.Model):
    follower = models.ForeignKey('accounts.Profile', related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey('accounts.Profile', related_name='followers', on_delete=models.CASCADE)
