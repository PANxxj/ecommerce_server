from django.urls import path
from .import api


urlpatterns = [
    path('cart_view/',api.CartView.as_view()),
    path('add_to_cart/',api.AddToCartView.as_view()),
    path('clear_cart/',api.ClearCartView.as_view()),
    path('update_cart_item/',api.UpdateCartItemView.as_view()),
    path('remove_item/',api.RemoveCartView.as_view()),
    path('create_order/',api.CreateOrder.as_view()),
    path('list/',api.OrderList.as_view()),
    path('get_all/',api.AllOrderList.as_view()),
    path('detail/',api.OrderDetail.as_view()),
]
