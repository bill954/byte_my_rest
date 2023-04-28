from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView

from admin_settings.models import Category, MeasureUnit
from admin_settings.serializers import DefinedConfigurations, SubCategorySerializer, MeasureUnitSerializer
from admin_settings.permissions import IsAdminOrReadOnly

class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = DefinedConfigurations

class MeasureUnitListCreateApiView(ListCreateAPIView):
    queryset = MeasureUnit.objects.all()
    serializer_class = MeasureUnitSerializer
    permission_classes = [IsAdminOrReadOnly]

class MeasureUnitRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = MeasureUnit.objects.all()
    serializer_class = MeasureUnitSerializer
    permission_classes = [IsAdminOrReadOnly]
