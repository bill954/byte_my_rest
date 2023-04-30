from django.urls import path, include, re_path

from admin_settings.views import ColorListCreateAPIView, ColorRetrieveUpdateDestroyAPIView, CategoryListCreateAPIView, CategoryRetrieveUpdateDestroy, SubcategoryListCreateAPIView, SubcategoryRetrieveUpdateDestroyAPIView, MeasureUnitListCreateApiView, MeasureUnitRetrieveUpdateDestroyAPIView 

urlpatterns = [
    # color
    path('colors/', ColorListCreateAPIView.as_view(), name='list_create_colors'),
    path('colors/<int:pk>', ColorRetrieveUpdateDestroyAPIView.as_view(), name='retrive_update_destroy_colors'),
    # categories
    path('categories/', CategoryListCreateAPIView.as_view(), name='list_create_categories'),
    path('categories/<int:pk>', CategoryRetrieveUpdateDestroy.as_view(), name='retrive_update_destroy_categories'),
    # measure units
    path('measure-units/', MeasureUnitListCreateApiView.as_view(), name='list_create_measure-units'),
    path('measure-units/<int:pk>/', MeasureUnitRetrieveUpdateDestroyAPIView.as_view(), name='retrive_update_destroy_measure-units'),
    # subcategories
    path('sub-categories/', SubcategoryListCreateAPIView.as_view(), name='list_create_subcategories'),
    path('sub-categories/<int:pk>', SubcategoryRetrieveUpdateDestroyAPIView.as_view(), name='retrive_update_destroy_subcategories'),
]