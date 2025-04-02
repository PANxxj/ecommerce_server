from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("supersecret/", admin.site.urls),
    # path("api/v1/auth/", include("djoser.urls")),
    # path("api/v1/auth/", include("djoser.urls.jwt")),
    # path("api/v1/account/", include("apps.accounts.urls")),
    path("api/v1/products/", include("apps.products.urls")),
    path("api/v1/orders/", include("apps.orders.urls")),
    path("api/v1/user/", include("apps.users.urls")),
]


admin.site.site_header = "E-Commerce Admin"
admin.site.site_title = "E-Commerce Admin Portal"
admin.site.index_title = "Welcome to the E-Commerce Portal"


