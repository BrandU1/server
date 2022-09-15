from django.urls import path

from orders.views import OrderCreateAPIView, OrderAPIView

urlpatterns = [
    path('create/', OrderCreateAPIView.as_view()),
    path('<int:pk>/', OrderAPIView.as_view()),
]
