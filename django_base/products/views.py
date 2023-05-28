from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404

from django.db.models import Q, Count, Value, CharField
from django.db.models.functions import Concat

from products.models import Product
from products.serializers import ProductSerializer, SimpleProductSerializer
from products.permissions import IsSellerOrReadOnly, IsSeller

################################### These classes are not being used in this version. ###################################
############# They're not commented because I don't like how they look when commented, but they sould be.################

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
    # Permission classes can be a tuple or list, but it must always be an iterable.
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

########################################### End of currently unused classes. #############################################

class MyProductsViewSet(ModelViewSet):
    def get_permissions(self):
        if self.action in ['list', 'create']:
            return [IsSeller]
        else:
            return []
        
    def get_queryset(self):
        products = self.request.user.products.filter().order_by('id')
        
        if 'search' in self.request.query_params:
            products = products.filter(name__icontains = self.request.query_params['search'])
        
        if 'category' in self.request.query_params:
            products = products.filter(category = self.request.query_params['category'])

        if 'subcategory' in self.request.query_params:
            products = products.filter(subcategory = self.request.query_params['subcategory'])

        if 'color' in self.request.query_params:
            products = products.filter(color = self.request.query_params['color'])

        if 'measure_unit' in self.request.query_params:
            products = products.filter(measure_unit = self.request.query_params['measure_unit'])
            
        order_by = self.request.query_params.get('order_by', 'id')
        return products.order_by(order_by)
    
    def get_serializer_class(self):
        if self.action == 'list':
            return SimpleProductSerializer
        
        else:
            return ProductSerializer
        
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['owner'] = request.user.pk
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
    # action decorator will turn this method into a view that executes an action in the dataset when it's accessed
    @action(detail=True, methods=['patch'], url_path='mark-unmark-distinguished')
    def mark_unmark_distinguished(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_distinguished:
            instance.is_distinguished = False
            instance.save()
            return Response('Product marked as not distinguished', status=status.HTTP_200_OK)
        
        if not instance.is_distinguished:        
            if instance.owner.products.filter(is_distinguished=True, is_deleted=False).count() >= 3:
                return Response('Already 3 products are distinguished', status=status.HTTP_400_BAD_REQUEST)
            else:
                instance.is_distinguished = True
                print('--------- heree -----------')
                print(instance)
                print(instance.is_distinguished)
                instance.save()
                return Response('Product marked as distinguished', status=status.HTTP_200_OK)

class ProductsViewSet(ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
#    serializer_class = ProductSerializer
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductSerializer
        else:
            return SimpleProductSerializer
    
    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_superuser:
            products = Product.objects.filter(owner__documentation__status='approved', is_deleted=False).order_by('id')
        else:
            products = Product.objects.filter(owner__documentation__status='approved', is_deleted=False, is_banned=False).order_by('id')
            
        if 'search' in self.request.query_params:
            products = (products.annotate(search_field = 
                            Concat('name', Value(' '), 
                            'owner__first_name', Value(' '), 
                            'owner__last_name'))
                            .filter(search_field__icontains = self.request.query_params['search']))

        if 'category' in self.request.query_params:
            products = products.filter(category = self.request.query_params['category'])

        if 'subcategory' in self.request.query_params:
            products = products.filter(subcategory = self.request.query_params['subcategory'])

        if 'color' in self.request.query_params:
            products = products.filter(color = self.request.query_params['color'])

        if 'measure_unit' in self.request.query_params:
            products = products.filter(measure_unit = self.request.query_params['measure_unit'])

        order_by = self.request.query_params.get('order_by', 'id')
        products = products.order_by(order_by)

        return products
    
    @action(detail=True, methods=['patch'], url_path='ban-unban-product', permission_classes=[IsAdminUser])
    def ban_unban_product(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_banned == True:
            instance.is_banned = False
            instance.save()
            return Response('Product is unbanned', status=status.HTTP_200_OK)
        elif instance.is_banned == False:
            instance.is_banned = True
            instance.save()
            return Response('Product is banned', status=status.HTTP_200_OK)