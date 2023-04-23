from rest_framework import serializers
from users.models import User, UserProfile, UserDocumentation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
class UserDocumentationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDocumentation
        fields = ['document_type', 'document_identifier', 'front_image', 'back_image']
        
class UserDocumentationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDocumentation
        fields = '__all__'
        
class UserDocumentationListSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username')
    
    class Meta:
        model = UserDocumentation
        fields = ['id', 'user_name', 'document_type', 'document_identifier', 'front_image', 'back_image']
    
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'user_type', 'is_active', 'date_joined']
        
