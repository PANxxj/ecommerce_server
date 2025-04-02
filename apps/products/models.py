import random
import string

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.helper.models import TimeStampedUUIDModel

User = get_user_model()

######## Master Category model ######

class Category(TimeStampedUUIDModel):
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True) 
    
    def __str__(self):
        return self.name

######### Product model ########
class Product(TimeStampedUUIDModel):

    user = models.ForeignKey(
        User,
        verbose_name=_("Vender"),
        related_name="Product",
        on_delete=models.DO_NOTHING,
    )
    category = models.ForeignKey(to=Category,on_delete=models.SET_NULL,null=True)
    title = models.CharField(verbose_name=_("Product Title"), max_length=250)
    stock_quantity = models.PositiveIntegerField(default=0)
    description = models.TextField(
        verbose_name=_("Description"),
        default="Default description...update me please....",
    )
    price = models.DecimalField(
        verbose_name=_("Price"), max_digits=8, decimal_places=2, default=0.0
    )
    discount_price = models.DecimalField(
        verbose_name=_("Price"), max_digits=8, decimal_places=2, default=0.0
    )
    rating = models.CharField(max_length=10,null=True,blank=True)
    photo1 = models.URLField(
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(default=True) 
    views = models.IntegerField(verbose_name=_("Total Views"), default=0)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    # def save(self, *args, **kwargs):
    #     self.title = str.title(self.title)
    #     self.ref_code = "".join(
    #         random.choices(string.ascii_uppercase + string.digits, k=10)
    #     )
    #     super(Product, self).save(*args, **kwargs)



class ProductViews(TimeStampedUUIDModel):
    ip = models.CharField(verbose_name=_("IP Address"), max_length=250)
    product = models.ForeignKey(
        Product, related_name="product_views", on_delete=models.CASCADE
    )

    def __str__(self):
        return (
            f"Total views on - {self.product.title} is - {self.product.views} view(s)"
        )

    class Meta:
        verbose_name = "Total Views on Product"
        verbose_name_plural = "Total Product Views"
