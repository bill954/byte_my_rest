from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from products.views import ProductListCreateAPIView, ProductRetrieveUpdateDestroyAPIView, ProductListAPIView, BanProductsAdminView, MyProductsViewSet, ProductsViewSet, celery_test_view

router = DefaultRouter()
router.register('my-products', MyProductsViewSet, basename='my-products')
router.register('all-products', ProductsViewSet, basename='products-view-set')

urlpatterns = [
    path('', include(router.urls)),
    path('celery-test/', celery_test_view)
#    path('', ProductListCreateAPIView.as_view(), name='list-create-my-products'),
#    path('<int:pk>', ProductRetrieveUpdateDestroyAPIView.as_view(), name='retrieve-update-destroy-products'),
#    path('list/', ProductListAPIView.as_view(), name='list-all-products'),
#    path('ban/<int:pk>', BanProductsAdminView.as_view(), name='admin-ban-product'),    
]