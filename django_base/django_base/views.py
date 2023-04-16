from django.shortcuts import render
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from allauth.account.models import EmailAddress

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from allauth.account.views import ConfirmEmailView
from dj_rest_auth.registration.serializers import VerifyEmailSerializer

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
    
@receiver(post_save, sender=User)
def create_profile(sender, instance, **kwargs):
    if kwargs['created'] and instance.is_superuser:
        EmailAddress.objects.create(user=instance, email=instance.email, verified=True, primary=True)