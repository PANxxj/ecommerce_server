
from django.db import models
from apps.helper.models import TimeStampedUUIDModel
from apps.products import models as product_models
from django.contrib.auth import get_user_model
from apps.helper import choices

User = get_user_model()
    
######### Order model ########

class OrderData(TimeStampedUUIDModel):
    order_id = models.CharField(max_length=20,null=True,blank=True)
    customer = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='orders',null=True,blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=choices.OrderStatus.choices, default=choices.OrderStatus.PROCESSING)
    payment_status = models.CharField(max_length=50, choices=choices.PaymentStatus.choices, default=choices.OrderStatus.PENDING)
    total_price = models.IntegerField()
    
    shipping_address = models.TextField(null=True,blank=True)
    shipping_method = models.CharField(max_length=100,null=True,blank=True)
    shipping_cost = models.IntegerField(default=0,null=True,blank=True)
    
    coupon_code = models.CharField(max_length=100, null=True, blank=True)
    discount_amount = models.IntegerField(default=0)
    
    payment_method = models.CharField(max_length=100)
    payment_date = models.DateTimeField(null=True, blank=True)
    dod = models.DateField(null=True, blank=True)
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    payment_gateway = models.CharField(max_length=100, null=True, blank=True)

    order_notes = models.TextField(null=True, blank=True)
    tracking_number = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Order {self.customer.email}"

    def get_total_price(self):
        """Calculate the total price of the order including shipping and discounts"""
        return self.total_price + self.shipping_cost - self.discount_amount


######### Order Item model ########

class OrderItem(TimeStampedUUIDModel):
    order = models.ForeignKey(to=OrderData, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(to=product_models.Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.IntegerField()
    discount = models.IntegerField(default=0)

    def get_item_total(self):
        return (self.price - self.discount) * self.quantity

    def __str__(self):
        return f"{self.product.title} - {self.quantity} x {self.price}"
    
    
class OrderStep(models.Model):
    odering = models.CharField(max_length=10,null=True,blank=True)
    order = models.ForeignKey(to=OrderData, on_delete=models.CASCADE, related_name='steps')
    status = models.CharField(max_length=30,null=True,blank=True)
    description = models.TextField()
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.status} - {self.order.id}"
    
   
######### Cart model ######## 
class Cart(TimeStampedUUIDModel):
    user = models.ForeignKey(to=User, null=True, blank=True, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)  

    def __str__(self):
        return f"Cart for {self.user.email if self.user else 'Guest'}"


    def get_total(self):
        """Calculate the total price of items in the cart."""
        total = sum(item.get_total() for item in self.cart_items.all())
        return total

    def clear_cart(self):
        """Clear all items from the cart."""
        self.cart_items.all().delete()
        

######### Cart Item model ########
class CartItem(TimeStampedUUIDModel):
    cart = models.ForeignKey(Cart, related_name='cart_items', on_delete=models.CASCADE)
    product = models.ForeignKey(to=product_models.Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.title} - {self.quantity}"

    def get_total(self):
        """Calculate the total price for this item (product price * quantity)."""
        return self.product.price * self.quantity

    def update_quantity(self, quantity):
        """Update the quantity of the product in the cart."""
        self.quantity = quantity
        self.save()
    
    def remove_from_cart(self):
        """Remove the item from the cart."""
        self.delete()