from django.urls import path

from orders.views import OrderCreateAPIView, OrderAPIView

urlpatterns = [
    path('', OrderCreateAPIView.as_view()),
    path('<int:pk>/', OrderAPIView.as_view()),
]
