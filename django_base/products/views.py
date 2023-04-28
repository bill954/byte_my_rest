from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from products.models import Product
from products.serializers import ProductSerializer
from products.permissions import IsSeller


class ProductListCreateAPIView(ListCreateAPIView):
#    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsSeller]
        
    def get_queryset(self):
        return self.request.products.all()
    
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)