from django.urls import path
from products import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView 


urlpatterns = [
    path('', views.home, name='home'),
    path('add_to_cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('update_cart/<int:pk>/', views.update_cart, name='update_cart'),
    path('remove_from_cart/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('add_to_wishlist/<int:product_pk>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('profile/', views.profile, name='profile'),
    path('accounts/profile/', views.profile, name='profile'),
    path('login/', views.login_view, name='login'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('product/update/<int:pk>/', views.product_update, name='product_update'),
    path('product/<int:pk>/edit/', views.product_update, name='product_update'),
    path('products/', views.product_list, name='products'),  # Consolidated name for the products list
    path('products/<int:pk>/', views.product_detail, name='product_detail'),  # Single product detail view
    path('product/<int:pk>/edit/', views.product_form, name='product_edit'),
    path('product/new/', views.product_form, name='product_new'),
    path('product/<int:pk>/delete/', views.product_delete, name='delete_product'),
    path('checkout/', views.checkout, name='checkout'),
    path('cart/', views.cart, name='cart'),
    path('order-confirmation/', views.order_confirmation, name='order_confirmation'),
    path('signup/', views.signup, name='signup'),
    path('shop/', views.shop, name='shop'),
    path('process_order/', views.process_order, name='process_order'),
]

