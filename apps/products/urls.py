from django.urls import path
from . import api

urlpatterns = [
    path('create/',api.CreateProductAPI.as_view()),
    path('update/<int:pk>/',api.UpdateProductAPI.as_view()),
    path('list/',api.ProductListViewAPI.as_view()),
    path('delete/',api.DeleteProduct.as_view()),
    path('get/',api.ProductViewAPI.as_view()),
]
