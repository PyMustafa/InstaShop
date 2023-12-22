from django.urls import path
from . import views
urlpatterns = [
    path('', views.store, name='store'),
    path('cat/<slug:category_slug>/', views.store, name='category-products'),
    path('cat/<slug:category_slug>/<slug:product_slug>/', views.product_details, name='product-details'),

    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
]