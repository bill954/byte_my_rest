from rest_framework import serializers

from admin_settings.models import Category, SubCategory, MeasureUnit
        
class DefinedConfigurations(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=70)
    
class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'

class MeasureUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasureUnit
        fields = '__all__'