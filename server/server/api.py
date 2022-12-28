from django.urls import path, include

urlpatterns = [
    path('auth/', include('auths.urls')),
    path('accounts/', include('accounts.urls'), name='accounts'),
    path('products/', include('products.urls'), name='products'),
    path('communities/', include('communities.urls'), name='communities'),
    path('search/', include('search.urls'), name='search'),
    path('orders/', include('orders.urls'), name='orders'),
    path('events/', include('events.urls'), name='events'),
    path('services/', include('services.urls'), name='services'),
]
