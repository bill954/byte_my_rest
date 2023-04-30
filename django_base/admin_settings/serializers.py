from rest_framework import serializers

from admin_settings.models import Color, Category, SubCategory, MeasureUnit

# Generic serializer that can be used for every model that has only a name and an id.
class DefinedConfigurations(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=70)
    
class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'

class MeasureUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasureUnit
        fields = '__all__'