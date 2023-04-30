from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView

from admin_settings.models import Category, MeasureUnit, SubCategory, Color
from admin_settings.serializers import DefinedConfigurations, SubCategorySerializer, MeasureUnitSerializer, CategorySerializer, ColorSerializer
from admin_settings.permissions import IsAdminOrReadOnly

class ColorListCreateAPIView(ListCreateAPIView):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    permission_classes = [IsAdminOrReadOnly]

class ColorRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    permission_classes = [IsAdminOrReadOnly]

class CategoryListCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

class CategoryRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = DefinedConfigurations
    permission_classes = [IsAdminOrReadOnly]

class MeasureUnitListCreateApiView(ListCreateAPIView):
    queryset = MeasureUnit.objects.all()
    serializer_class = MeasureUnitSerializer
    permission_classes = [IsAdminOrReadOnly]

class MeasureUnitRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = MeasureUnit.objects.all()
    serializer_class = MeasureUnitSerializer
    permission_classes = [IsAdminOrReadOnly]

class SubcategoryListCreateAPIView(ListCreateAPIView):
    def get_queryset(self):
        if 'category' not in self.request.query_params:
            return SubCategory.objects.all()
        else:
            return SubCategory.objects.filter(category__id=self.request.query_params['category'])
        
    serializer_class = SubCategorySerializer
    permission_classes = [IsAdminOrReadOnly]

class SubcategoryRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = [IsAdminOrReadOnly]
