from django.contrib import admin
from . import models as product_models


admin.site.register(product_models.Category)
admin.site.register(product_models.Product)