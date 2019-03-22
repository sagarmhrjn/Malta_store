from django.urls import path
from store import views

urlpatterns = [
    # Catalog view and adding items to cart
    path('', views.catalog, name='catalog'),
    # New product
    path('product/new/', views.addItem, name='add-product'),
    # Details of product
    path('product/<int:pk>/', views.details, name='product-details'),
    # Edit product
    path('product/<int:pk>/edit/', views.editProduct, name='product-edit'),
    # Delete product
    path('product/<int:pk>/delete/', views.deleteProduct, name='product-delete'),
    # List of cart items
    path('cart/', views.cart, name="cart"),
    # Removing cart
    path('cart/remove/', views.removefromcart, name="remove"),
    # for checkout
    path('cart/checkout/', views.checkout, name="checkout"),
    # for complete order
    path('cart/checkout/complete/', views.completeOrder, name="complete_order"),
    # Edit Order
    path('order/<int:pk>/edit/', views.editOrder, name='order-edit'),
    # Delete Order
    path('order/<int:pk>/delete/', views.deleteOrder, name='order-delete'),
    path('admin_panel/', views.adminDashboard, name="admin"),

]
