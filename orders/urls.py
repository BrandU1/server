from django.urls import path

from orders.views import OrderCreateAPIView, OrderAPIView, OrderTossConfirmAPIView, TrackingAPIView

urlpatterns = [
    path('toss/create/', OrderCreateAPIView.as_view()),
    path('toss/confirm/', OrderTossConfirmAPIView.as_view()),
    path('<int:pk>/', OrderAPIView.as_view()),
    path('<int:pk>/tracking/', TrackingAPIView.as_view()),
]
