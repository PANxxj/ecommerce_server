from rest_framework import serializers
from . import models as order_models
from apps.products import serializers as product_serializers
import datetime

class CartItemSerializer(serializers.ModelSerializer):
    product = product_serializers.ProductSerializer()

    class Meta:
        model = order_models.CartItem
        fields = ['id', 'product', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(source='cart_items.all', many=True)

    class Meta:
        model = order_models.Cart
        fields = ['id', 'user', 'is_active', 'cart_items']

class OrderItemSerializer(serializers.ModelSerializer):
    product = product_serializers.ProductSerializer()
    image = serializers.SerializerMethodField()

    class Meta:
        model = order_models.OrderItem
        fields = ['id', 'product', 'quantity', 'price','image']
        
    def get_image(self,obj):
        return obj.product.photo1
        
class PostOrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = order_models.OrderItem
        fields = ['product', 'quantity', 'price']

class OrderDataSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(source='items.all', many=True)
    id  = serializers.SerializerMethodField(read_only=True)
    date  = serializers.SerializerMethodField(read_only=True)
    total = serializers.SerializerMethodField()
    steps = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    customer = serializers.SerializerMethodField()

    class Meta:
        model = order_models.OrderData
        # fields = ['id', 'order_id', 'customer', 'order_date', 'status', 'total_price', 'shipping_address', 'shipping_method', 'order_items']
        fields = ['id', 'customer', 'date', 'status', 'total', 'shipping_address', 'shipping_method', 'items','steps','order_id']
    
    def get_id(self,obj):
        return obj.pk
    
    def get_customer(self,obj):
        return obj.customer.full_name
    
    def get_total(self,obj):
        return obj.total_price
    
    def get_status(self,obj):
        steps_data = order_models.OrderStep.objects.filter(order =obj,completed=True).order_by('odering').last()
        if steps_data:
            return steps_data.status
        return 'Processing'

    
    def get_steps(self,obj):
        steps = order_models.OrderStep.objects.filter(order=obj).order_by('-odering').values('status','description','completed','date','time')
        return steps
    
    def get_date(self,obj):
        return datetime.datetime.strftime(obj.order_date,'%d %b %y, %I:%M %p')
    
        


class PostOrderDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = order_models.OrderData
        fields = ['customer', 'total_price', 'shipping_address', 'shipping_method']



class OrderStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = order_models.OrderStep
        fields = ['id', 'status', 'description', 'date', 'time', 'completed']

class TrackingSerializer(serializers.Serializer):
    number = serializers.CharField()
    carrier = serializers.CharField()
    steps = OrderStepSerializer(many=True)

class OrderDataDetailsSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    # tracking = TrackingSerializer()

    class Meta:
        model = order_models.OrderData
        fields = [
            'id', 'order_id', 'order_date', 'status', 'shipping_address', 'total_price', 
            'coupon_code', 'discount_amount', 'payment_method', 'payment_date', 'dod', 'items',
            'transaction_id', 'payment_gateway', 'order_notes',        ]

    def to_representation(self, instance):
        """Override to adjust the API response to mock structure."""
        data = super().to_representation(instance)
        steps_data = order_models.OrderStep.objects.filter(order =instance,completed=True).order_by('odering').last()
        if steps_data:
            data['status'] = steps_data.status

        data['id'] = f"ORD-{instance.order_id}"
        data['date'] = instance.order_date.date().strftime('%Y-%m-%d')
        data['shippingAddress'] = instance.shipping_address
        data['subtotal'] = instance.total_price - instance.discount_amount  
        data['shipping'] = instance.shipping_cost 
        data['tax'] = instance.total_price * 0.08  #
        data['total'] = instance.get_total_price() 
        
        if instance:
            tracking_data = {
                'number': instance.tracking_number if instance.tracking_number else '',
                'carrier': 'Vendor Express',  # You can set this dynamically based on your use case
                'steps': OrderStepSerializer(instance.steps.all(), many=True).data
            }
            data['tracking'] = tracking_data
        else:
            data['tracking'] = {}

        return data



