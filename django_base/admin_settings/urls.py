from django.urls import path, include, re_path

from admin_settings.views import CategoryListAPIView, MeasureUnitListCreateApiView, MeasureUnitRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('categories/', CategoryListAPIView.as_view(), name='categories'),
    path('measure-units/', MeasureUnitListCreateApiView.as_view(), name='measure-units'),
    path('measure-units/<int:pk>/', MeasureUnitRetrieveUpdateDestroyAPIView.as_view(), name='measure-units'),
]