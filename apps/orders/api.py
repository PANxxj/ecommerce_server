from rest_framework import status
# from .models import Cart, CartItem, Product
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from . import serializers as order_serializers
from . import models as order_models
from apps.products import models as product_models
from apps.helper import functions,status_code,messages,keys
from rest_framework.response import Response


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            cart = order_models.Cart.objects.get(user=request.user, is_active=True)
            serializer = order_serializers.CartSerializer(cart)
            return Response(functions.ResponseHandling.success_response_message(messages.OPERATION_SUCCESS,serializer.data),status=status_code.status200)
        except order_models.Cart.DoesNotExist:
            return Response(functions.ResponseHandling.failure_response_message("No active cart found.",''), status=status_code.status404)

class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        
        try:
            cart = order_models.Cart.objects.get(user=request.user)
        except order_models.Cart.DoesNotExist:
            cart = order_models.Cart.objects.create(user=request.user)

        try:
            product = product_models.Product.objects.get(pk=product_id)
        except product_models.Product.DoesNotExist:
            return Response(functions.ResponseHandling.failure_response_message(messages.DATA_NOT_FOUND,''), status=status_code.status404)

        cart_item, created = order_models.CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity = quantity
            cart_item.save()

        return Response(functions.ResponseHandling.success_response_message('Item added to cart.',''), status=status_code.status201)

class UpdateCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart_item_id = request.data.get('cart_item_id')
        quantity = request.data.get('quantity')
        
        try:
            cart_item = order_models.CartItem.objects.get(id=cart_item_id, cart__user=request.user)
            cart_item.quantity = quantity
            cart_item.save()
            return Response(functions.ResponseHandling.success_response_message('Cart item updated.',''), status=status_code.status201)
        except order_models.CartItem.DoesNotExist:
            return Response(functions.ResponseHandling.failure_response_message(messages.DATA_NOT_FOUND,''), status=status_code.status404)

class ClearCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            cart = order_models.Cart.objects.get(user=request.user, is_active=True)
            cart.clear_cart()
            return Response(functions.ResponseHandling.success_response_message(messages.OPERATION_SUCCESS,''), status=status_code.status204)
        except order_models.Cart.DoesNotExist:
            return Response(functions.ResponseHandling.failure_response_message(messages.DATA_NOT_FOUND,''), status=status_code.status404)
        
class RemoveCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            product = request.data['id']
            cart = order_models.CartItem.objects.get(cart__user=request.user,product = product).delete()
            # cart.clear_cart()
            return Response(functions.ResponseHandling.success_response_message(messages.OPERATION_SUCCESS,''), status=status_code.status204)
        except order_models.Cart.DoesNotExist:
            return Response(functions.ResponseHandling.failure_response_message(messages.DATA_NOT_FOUND,''), status=status_code.status404)
        
        
class CreateOrder(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        print('rq',request.data)
        order_ser= order_serializers.PostOrderDataSerializer(data=request.data)
        if not order_ser.is_valid(raise_exception=False):
            errors = order_ser.errors
            errors = functions.error_message_function(errors)
            return Response(functions.ResponseHandling.failure_response_message('error',errors),status=status_code.status400)
        order = order_ser.save()
        
        items = request.data.get('order_items',[])
        if isinstance(items,list):
            ser = order_serializers.PostOrderItemSerializer(data=items,many=True)
            if not ser.is_valid(raise_exception=False):
                errors = ser.errors
                errors = functions.error_message_function(errors)
                return Response(functions.ResponseHandling.failure_response_message('error',errors),status=status_code.status400)
            ser.save(order=order)
        order.payment_status=keys.PAID
        order.save()
            
        return Response(functions.ResponseHandling.success_response_message(messages.OPERATION_SUCCESS,int(order.pk)), status=status_code.status200)

class OrderList(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        orders = order_models.OrderData.objects.filter(customer=request.user).order_by('-id')
        ser = order_serializers.OrderDataSerializer(orders,many=True)
        return Response(functions.ResponseHandling.success_response_message(messages.OPERATION_SUCCESS,ser.data), status=status_code.status200) 
    
    
class OrderDetail(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        id = request.GET.get('id')
        try:
            orders = order_models.OrderData.objects.get(pk=id)
        except order_models.OrderData.DoesNotExist:
            return Response(functions.ResponseHandling.failure_response_message(messages.DATA_NOT_FOUND,''), status=status_code.status404)
        ser = order_serializers.OrderDataDetailsSerializer(orders)
        return Response(functions.ResponseHandling.success_response_message(messages.OPERATION_SUCCESS,ser.data), status=status_code.status200)
    
    
class AllOrderList(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        orders = order_models.OrderData.objects.filter(items__product__user=request.user).order_by('-id')
        ser = order_serializers.OrderDataSerializer(orders,many=True)
        return Response(functions.ResponseHandling.success_response_message(messages.OPERATION_SUCCESS,ser.data), status=status_code.status200) 
     
     
        