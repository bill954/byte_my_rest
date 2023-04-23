from django.urls import path, include, re_path

from users.views import UserDocumentationView, UserDocumentationAdminView, UserListView, SellersListView

urlpatterns = [
    path('documentation/', UserDocumentationView.as_view(), name='user_documentation'),
    path('admin-documentation/', UserDocumentationAdminView.as_view(), name='user_documentation_admin'),
    path('', UserListView.as_view(), name='UserListView'),
    path('sellers/', SellersListView.as_view(), name='SellersListView'),
]