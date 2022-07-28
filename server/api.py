from django.urls import path, include

urlpatterns = [
    path('auth/', include('auths.urls')),
    path('accounts/', include('accounts.urls'), name='accounts'),
    path('products/', include('products.urls')),
    path('search/', include('search.urls')),
]
