from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from users.serializers import UserDocumentationUpdateSerializer, UserDocumentationSerializer, UserDocumentationListSerializer
from users.models import UserDocumentation

class UserDocumentationView(APIView):

    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        if not request.user.user_type == 'seller':
            return Response(['Only sellers have documentation'], status=status.HTTP_401_UNAUTHORIZED)
        if request.user.is_superuser:
            return Response(['Admins have no documentation'], status=status.HTTP_401_UNAUTHORIZED)
        if request.user.documentation.status == 'not uploaded':
            return Response(['Documentation not uploaded yet'], status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = UserDocumentationSerializer(request.user.documentation)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def patch(self, request):
        if not request.user.user_type == 'seller':
            return Response(['Only sellers have documentation'], status=status.HTTP_401_UNAUTHORIZED)
        if request.user.is_superuser:
            return Response(['Admins have no documentation'], status=status.HTTP_401_UNAUTHORIZED)
        
        if not all(('document_type' in request.data,
            'document_identifier' in request.data,
            'front_image' in request.data,
            'back_image' in request.data)):
            return Response(['Missing fields'], status=status.HTTP_400_BAD_REQUEST)
        
        serializer = UserDocumentationUpdateSerializer(request.user.documentation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.instance.status = 'uploaded'
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDocumentationAdminView(APIView):
    
    permission_classes = (IsAdminUser,)
    
    def get(self, request):
        user_documents = UserDocumentation.objects.filter(status='uploaded')
        serializer = UserDocumentationListSerializer(user_documents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request):
        if not 'document_id' in request.data:
            return Response('Missin document_id', status=status.HTTP_400_BAD_REQUEST)
        
        if not 'status' in request.data or request.data['status'] not in ['approved', 'rejected']:
            return Response('Missing status', status=status.HTTP_400_BAD_REQUEST)

        document_id = request.data['document_id']
        document_status = request.data['status']
        
        try:
            document = UserDocumentation.objects.get(id=document_id)
        except:
            return Response('Document not found', status=status.HTTP_404_NOT_FOUND)
        
        if document_status == 'rejected':
            if not 'rejected_reason'in request.data:
                return Response('Missing rejected reason', status=status.HTTP_400_BAD_REQUEST)
            document.rejection_reason = request.data['rejected_reason']
        else:
            document.rejection_reason = ''
        
        document.status = document_status
        document.save()
        return Response('Document status updated', status=status.HTTP_200_OK)