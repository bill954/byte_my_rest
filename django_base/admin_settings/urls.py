from django.urls import path, include, re_path

from admin_settings.views import CategoryListAPIView

urlpatterns = [
    path('categories/', CategoryListAPIView.as_view(), name='categories'),
]