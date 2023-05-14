from django.urls import path, include, re_path

from products.views import ProductListCreateAPIView, ProductRetrieveUpdateDestroyAPIView, ProductListAPIView, BanProductsAdminView

urlpatterns = [
    path('', ProductListCreateAPIView.as_view(), name='list-create-my-products'),
    path('<int:pk>', ProductRetrieveUpdateDestroyAPIView.as_view(), name='retrieve-update-destroy-products'),
    path('list/', ProductListAPIView.as_view(), name='list-all-products'),
    path('ban/<int:pk>', BanProductsAdminView.as_view(), name='admin-ban-product'),    
]