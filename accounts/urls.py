from django.urls import path

from accounts.views import (
    ProfileDetailAPIView, ProfileFollowAPIView, ProfileEditAPIView, ProfileAPIView, SetMainAddressAPIView,
    AddressListAPIView, AddressEditAPIView, ReviewListAPIView, ReviewAPIView, ProfilePointAPIView, NotifyAPIView,
    WishListAPIView, WishListListAPIView, BasketListAPIView, BasketAPIView, PostScrappedListAPIView,
    PostScrappedCreateAPIView,
)

urlpatterns = [
    path('me/', ProfileAPIView.as_view()),
    path('notify/', NotifyAPIView.as_view()),
    path('edit/', ProfileEditAPIView.as_view()),
    path('point/', ProfilePointAPIView.as_view()),
    path('summary/', ProfileDetailAPIView.as_view()),
    path('follow/', ProfileFollowAPIView.as_view()),
    path('address/', AddressListAPIView.as_view()),
    path('address/<int:pk>/', AddressEditAPIView.as_view()),
    path('address/<int:pk>/main/', SetMainAddressAPIView.as_view()),
    path('review/', ReviewListAPIView.as_view()),
    path('review/<int:pk>/', ReviewAPIView.as_view()),
    path('wishs/', WishListListAPIView.as_view()),
    path('wish/<int:pk>/', WishListAPIView.as_view()),
    path('scrapped/', PostScrappedListAPIView.as_view()),
    path('scrap/<int:pk>/', PostScrappedCreateAPIView.as_view()),
    path('baskets/', BasketListAPIView.as_view()),
    path('basket/<int:pk>/', BasketAPIView.as_view()),
]
