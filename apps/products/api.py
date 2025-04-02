from django.conf import settings
from rest_framework import generics
from rest_framework.views import APIView
from django.db.models import ProtectedError
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import AnonymousUser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.helper.pagination import ProductPagination
from . import serializers as product_serializers
from . import models as product_models
from apps.helper import functions,status_code,messages,keys
from django.db.models import Q
import json


class CreateProductAPI(generics.CreateAPIView):

    serializer_class=product_serializers.ProductCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        request_data=request.data.copy()
        category = request_data.pop('category')
        category = product_models.Category.objects.filter(name__icontains=category).first()
        request_data['user']=request.user.pk
        
        product_serializer = self.get_serializer(data=request_data)
        if not product_serializer.is_valid(raise_exception=False):
            errors = product_serializer.errors
            print('error',errors)
            errors=functions.error_message_function(errors)
            return Response(functions.ResponseHandling.failure_response_message(errors, ""), status=status_code.status400)
        
        obj = product_serializer.save(category=category)    
        return Response(functions.ResponseHandling.success_response_message(messages.OPERATION_SUCCESS, ''), status=status_code.status201)
    
    
class UpdateProductAPI(generics.UpdateAPIView):
    
    permission_classes = [IsAuthenticated]
    queryset=product_models.Product
    serializer_class=product_serializers.ProductCreateSerializer
    lookup_field=keys.PKID
    
    def update(self,request,*args,**kwargs):
        request_data=request.data.copy()
        category = request_data.pop('category')
        category = product_models.Category.objects.filter(name__icontains=category).first()
        buyer_instance=self.get_object()
        buyer_serializer =self.get_serializer(buyer_instance,data=request_data,partial=True)
        if not buyer_serializer.is_valid(raise_exception=False):
            errors=buyer_serializer.errors
            errors=functions.error_message_function(errors)
            return Response(functions.ResponseHandling.failure_response_message(errors, ""), status=status_code.status400)
        buyer_serializer.save(category=category)
        return Response(functions.ResponseHandling.success_response_message(messages.UPDATED_SUCCESSFULLY, ""), status=status_code.status201)

class DeleteProduct(APIView):
    
    def delete(self,request):
        id = request.GET.get('id')
        product = product_models.Product.objects.get(pk=id).delete()
        return Response (functions.ResponseHandling.success_response_message(messages.OPERATION_SUCCESS, ''), status=status_code.status200)
    
    


class ProductListViewAPI(generics.ListAPIView):

    serializer_class=product_serializers.ProductSerializer
    pagination_class=ProductPagination
    
    def list(self, request, *args, **kwargs):
        search=request.GET.get('search',None)
        category=request.GET.get('category',None)

        queryset = product_models.Product.objects.all().order_by('-pk')
            
        if search :
            queryset = queryset.filter(Q(title__icontains=search) | Q (description__icontains=search))
        if category :
            queryset = queryset.filter(Q(category__name__icontains=search))
            
        serializer = self.get_serializer(queryset, many=True)
        # page, page_info = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        
        data = serializer.data

        if not queryset:
            return Response(functions.ResponseHandling.failure_response_message(messages.DATA_NOT_FOUND,[] ), status=status_code.status200)
        return Response (functions.ResponseHandling.success_response_message(messages.LIST_SENT, data), status=status_code.status200)
    
    
    

class ProductViewAPI(generics.RetrieveAPIView):

    serializer_class=product_serializers.ProductSerializer
    pagination_class=ProductPagination
    
    def get(self, request, *args, **kwargs):
        id=request.GET.get('id',None)
   
        queryset = product_models.Product.objects.get(pk=id)
            
            
        serializer = self.get_serializer(queryset)
        
        data = serializer.data

        if not queryset:
            return Response(functions.ResponseHandling.failure_response_message(messages.DATA_NOT_FOUND,[] ), status=status_code.status200)
        return Response (functions.ResponseHandling.success_response_message(messages.LIST_SENT, data), status=status_code.status200)

       
   

    
    

