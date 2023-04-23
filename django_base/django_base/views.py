from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from allauth.account.views import ConfirmEmailView

from dj_rest_auth.registration.serializers import VerifyEmailSerializer
from dj_rest_auth.registration.views import RegisterView

from users.models import UserDocumentation

class HelloWorldView(APIView):
    def get(self, request):
        return Response({'message': 'Hellow, world!'}, status=status.HTTP_200_OK)
    
    def post(self, request):
        if 'hello' in request.data:
            return Response({'message': request.data['hello']}, status=status.HTTP_200_OK)
        return Response({'message': 'Hello, POST!'}, status=status.HTTP_200_OK)
    
class EmailVerification(APIView, ConfirmEmailView):
    
    def get(self, request, key):
        return render(request, 'registration/verify_email.html', context={'key': key, 'BASE_URL': '127.0.0.1.8000'})
    
    def post(self, request, *args, **kwargs):
        serializer = VerifyEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.kwargs['key'] = serializer.validated_data['key']
        confirmation = self.get_object()
        confirmation.confirm(self.request)
        return Response({'detail': 'ok'}, status=status.HTTP_200_OK)
    
class CustomRegisterView(RegisterView):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = self.get_response_data(user)
        
        user.first_name = request.data.get('first_name', '')
        user.last_name = request.data.get('last_name', '')
        user.user_type = request.data.get('user_type', 'buyer')
        user.save()
        
        if user.user_type == 'seller':
            UserDocumentation.objects.create(user=user)
        
        if data:
            response = Response(status=status.HTTP_201_CREATED, headers=headers)
        
        else:
            response = Response(status=status.HTTP_204_NO_CONTENT, headers=headers)

        return response