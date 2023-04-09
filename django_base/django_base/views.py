from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

class HelloWorldView(APIView):
    def get(self, request):
        return Response({'message': 'Hellow, world!'}, status=status.HTTP_200_OK)
    
    def post(self, request):
        if 'hello' in request.data:
            return Response({'message': request.data['hello']}, status=status.HTTP_200_OK)
        return Response({'message': 'Hello, POST!'}, status=status.HTTP_200_OK)