from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser

from django.db.models import Q, Count, Value, CharField
from django.db.models.functions import Concat

from products.models import Product
from products.serializers import ProductSerializer, SimpleProductSerializer
from products.permissions import IsSellerOrReadOnly

class ProductListCreateAPIView(ListCreateAPIView):
#    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsSellerOrReadOnly]

    # Redefine get_queryset and create methods inherited from ListCreateAPIView to make sure
    # that the owner of the products is the one that is loged in.        
    def get_queryset(self):
        return self.request.user.products.all()

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['owner'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class ProductRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    #queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsSellerOrReadOnly]
    
    def get_queryset(self):
        return Product.objects.filter(owner=self.request.user.id)
    
    def get(self, request, pk):
        obj = Product.objects.filter(id=pk)
        if obj:
            if obj[0].owner == self.request.user or self.request.user.is_superuser or obj[0].is_banned == False:
                serializer = self.get_serializer(obj[0])
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif obj[0].is_banned == True:
                return Response({'error': 'Product not available'}, status=status.HTTP_403_FORBIDDEN)
        return Response({'detail': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)

class ProductListAPIView(ListAPIView):
    # queryset = Product.objects.all()
    serializer_class = SimpleProductSerializer
    permission_classes = [IsSellerOrReadOnly]
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            products = Product.objects.all()
        else:
            products = Product.objects.filter(is_banned=False)
            products = products.filter(owner__documentation__status='approved')
        
        # Here go the filters got from query_params
        if 'search' in self.request.query_params:
           products = (products.annotate(full_search_field = Concat('name', 
                                                            Value(' '),'category__name', 
                                                            Value(' '),'subcategory__name',
                                                            Value(' '),'owner__first_name',
                                                            Value(' '),'description', 
                                                            output_field = CharField()))
                .filter(full_search_field__icontains = self.request.query_params['search']))
           
        if 'order_by' in self.request.query_params:
            order_by = self.request.query_params['order_by']
            if order_by not in ['price', 'creation_time']:
                return Response({'error': 'order_by must be first_name, last_name or date_joined'}, status=status.HTTP_400_BAD_REQUEST)            
            products = products.order_by(order_by)
        
        return products
    
class BanProductsAdminView(APIView):
    permission_classes = [IsAdminUser]
    
    def patch(self, request, pk):
        if not 'is_banned' in request.data:
            return Response({'error': 'is_banned field is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if request.data['is_banned'].lower() not in ['true', 'false']:
            return Response({'error': 'is_banned must be True or False'})
        
        product = get_object_or_404(Product, pk=pk)
        product.is_banned = request.data['is_banned']
        product.save()
        
        return Response({'data': 'The banned state is: ' + request.data['is_banned']}, status=status.HTTP_200_OK)
