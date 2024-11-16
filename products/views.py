from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .models import Cart
from .models import Product
from .forms import ProductForm
from .models import Product, Category, Cart
from .models import Order
from .models import Wishlist
from .models import Product, Review
from django.views.generic import ListView
from django.views.decorators.http import require_POST

# Home page view
def home(request):
    products = Product.objects.all()  # Adjust to match your model
    return render(request, 'products/home.html', {'products': products})


def profile(request):
    return render(request, 'profile.html')
  

def home(request):
    products = Product.objects.all()  # Get all products
    return render(request, 'products/home.html', {'products': products})

# Order confirmation page
def order_confirmation(request):
    return render(request, 'products/order_confirmation.html')


def process_order(request):
    if request.method == 'POST':
        # Logic for processing the order goes here
        return redirect('order_confirmation')  # Replace with your desired URL name
    return redirect('checkout')  # Fallback in case of an invalid request


def shop(request):
    products = Product.objects.all()
    return render(request, 'products/shop.html', {'products': products})


# Checkout page
def checkout(request):
    cart = request.session.get('cart', {})
    
    # Debug: Print the cart session data
    print("Cart session data:", cart)  # This will display the cart data in your console/terminal
    
    cart_items = []
    cart_total = 0

    # If the cart isn't empty, fetch the products
    if cart:
        product_ids = cart.keys()
        products = Product.objects.filter(pk__in=product_ids)
        for product in products:
            quantity = cart[str(product.pk)]
            cart_items.append({'product': product, 'quantity': quantity})
            cart_total += product.price * quantity

    if request.method == 'POST':
        # Clear the session-based cart on checkout
        request.session['cart'] = {}
        return redirect('order_confirmation')

    return render(request, 'products/checkout.html', {
        'cart_items': cart_items,
        'cart_total': cart_total
    })

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to the homepage after successful login
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})




def profile(request):
    orders = Order.objects.filter(user=request.user).order_by('-date_ordered')
    return render(request, 'products/profile.html', {'orders': orders})


# Product list view with pagination and category filtering
def product_list(request, category_id=None):
    products = Product.objects.all()
    query = request.GET.get('q', '')
    if query:
        products = products.filter(name__icontains=query)

    if category_id:
        products = products.filter(category_id=category_id)

    paginator = Paginator(products, 8)  # 8 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()  # Get all categories for the dropdown

    return render(request, 'products/product_list.html', {
        'page_obj': page_obj,
        'categories': categories,
    })

# Product details view

def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    reviews = Review.objects.filter(product=product)
    
    if request.method == 'POST' and request.user.is_authenticated:
        rating = request.POST.get('rating')
        review_text = request.POST.get('review_text')
        Review.objects.create(
            product=product,
            user=request.user,
            rating=rating,
            review_text=review_text
        )
        return redirect('product_detail', pk=product.pk)

    return render(request, 'products/product_detail.html', {'product': product, 'reviews': reviews})




# Function to create a new product (admin or owner)
def product_create(request):
    if request.method == 'POST':
        # Logic to handle product creation (add form handling here)
        pass
    return render(request, 'products/product_form.html')

# Function to update an existing product (admin or owner)

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', pk=product.pk)  # Redirect after saving
    else:
        form = ProductForm(instance=product)  # Initialize form for GET request

    return render(request, 'products/product_update.html', {'form': form, 'product': product})

# Function to delete a product
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('products')  # Redirect after deletion
    return render(request, 'products/product_confirm_delete.html', {'product': product})

# User signup view
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created successfully!")
            return redirect('login')  # Redirect to login page after successful sign-up
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})




# Product form (for creating/updating products)
def product_form(request, pk=None):
    if pk:
        product = get_object_or_404(Product, pk=pk)
    else:
        product = Product()  # For creating a new product

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)

    return render(request, 'products/product_form.html', {'form': form, 'product': product})


def product_list(request):
    query = request.GET.get('q')
    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)

    
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    return render(request, 'products/product_list.html', {'products': products})


# Function to add a product to the cart
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    # Using session to store the cart as a dictionary {product_id: quantity}
    cart = request.session.get('cart', {})

    # Check if product is already in cart and update its quantity
    if product.pk in cart:
        cart[product.pk] += 1  # Increase quantity by 1 (can be modified as needed)
    else:
        cart[product.pk] = 1  # Add new product with quantity 1

    request.session['cart'] = cart
    return redirect('cart')  # Redirect to cart page


def cart(request):
    cart = request.session.get('cart', {})
    cart_items = []  # List to hold cart item details
    cart_total = 0  # Total cost of all items in the cart

    # Iterate over each item in the cart
    for product_pk, quantity in cart.items():
        try:
            product = Product.objects.get(pk=product_pk)  # Fetch the product using its primary key
            item_total = product.price * quantity  # Calculate the total price for this item
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total': item_total,
            })
            cart_total += item_total  # Add to the overall cart total
        except Product.DoesNotExist:
            continue  # Skip this item if the product no longer exists

    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
    }
    return render(request, 'products/cart.html', context)



# Function to update the quantity of a product in the cart
def update_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart_items = Cart.objects.filter(user=request.user, product=product)

    new_quantity = int(request.POST.get('quantity', 1))
    if cart_items.exists():
        cart_item = cart_items.first()  # Get the cart item for the logged-in user
        if new_quantity > 0:
            cart_item.quantity = new_quantity  # Update quantity in the database
            cart_item.save()
        else:
            cart_item.delete()  # Remove the item if the quantity is 0 or less

    # Update session cart after the database update
    cart = request.session.get('cart', {})
    if new_quantity > 0:
        cart[product.pk] = new_quantity  # Update session cart
    else:
        if product.pk in cart:
            del cart[product.pk]  # Remove from session cart if quantity is 0

    request.session['cart'] = cart  # Save updated cart in session
    return redirect('cart')  # Redirect back to the cart page


def remove_from_cart(request, pk):
    try:
        cart_item = Cart.objects.get(product__pk=pk, user=request.user)
        cart_item.delete()  # Remove the item from the cart
    except Cart.DoesNotExist:
        pass  # Handle the case where the cart item doesn't exist
    
    return redirect('cart') 

# Class-based view for listing products (with search functionality)
class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset




def add_to_wishlist(request, product_pk):
    product = Product.objects.get(pk=product_pk)
    wishlist = request.session.get('wishlist', [])
    
    if product.pk not in wishlist:  # Prevent duplicate entries
        wishlist.append(product.pk)
    
    request.session['wishlist'] = wishlist
    return redirect('wishlist')

def wishlist(request):
    wishlist_products = Product.objects.filter(pk__in=request.session.get('wishlist', []))
    return render(request, 'wishlist.html', {'wishlist_products': wishlist_products})
