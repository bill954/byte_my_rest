from django.urls import path, include, re_path

from products.views import ProductListCreateAPIView

urlpatterns = [
    path('', ProductListCreateAPIView.as_view(), name='products'),
]