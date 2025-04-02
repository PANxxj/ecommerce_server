from django.contrib import admin
from . import models as orders_models


admin.site.register(orders_models.Cart)
admin.site.register(orders_models.CartItem)
admin.site.register(orders_models.OrderData)
admin.site.register(orders_models.OrderItem)
admin.site.register(orders_models.OrderStep)