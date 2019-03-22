from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from store.models import Product, Order


from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import ProductForm


# Product CRUD

@login_required
def addItem(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        print(dir(form))
        if form.is_valid():
            form.save()
        return redirect('catalog')

    else:
        form = ProductForm()
    return render(request, 'store/add-product.html', {'form': form})


def details(request, pk):
    item = get_object_or_404(Product, id=pk)
    return render(request, 'store/details.html', {'item': item})


@login_required
def editProduct(request, pk):
    item = get_object_or_404(Product, id=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('product-details', item.id)
    else:
        form = ProductForm(instance=Product)
    return render(request, 'store/edit-product.html', {'item': item})


@login_required
def deleteProduct(request, pk):
    item = get_object_or_404(Product, id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('catalog')

    return render(request, 'store/confirmation_delete.html', {'item': item})


# CART
def cartItems(cart):    # takes cart session key as a parameter
    items = []
    for item in cart:
        # append the actual cart object per cart object id to items array
        items.append(Product.objects.get(id=int(item)))
    return items


def priceCart(cart):
    cart_items = cartItems(cart)
    price = 0
    for item in cart_items:
        price += item.price
    return price


def getItemsList(cart):
    cart_items = cartItems(cart)
    items_list = ""
    for item in cart_items:
        items_list += str(item.name)
        items_list += ","
    return items_list


def removefromcart(request):
    request.session.set_expiry(0)
    obj_to_remove = int(request.POST['obj_id'])
    # index() method returns the index of the element in the list.
    obj_indx = request.session['cart'].index(int(obj_to_remove))
    # pop() method returns the item present at the given index. This item will be removed the list.
    request.session['cart'].pop(obj_indx)
    return redirect("cart")


def catalog(request):
    # check if cart is already within the session
    if 'cart' not in request.session:
        cart = []
        request.session['cart'] = []
    cart = request.session['cart']
    # make sure the session doesn't expire until the user closes the browser window
    request.session.set_expiry(0)

    store_items = Product.objects.all()
    ctx = {'store_items': store_items, 'cart': cart, 'cart_size': len(cart)}
    main_page = render(request, 'store/main.html', ctx)

    if request.method == 'POST':
        # convert it into integer so that we can have actual numerical id
        cart.append(int(request.POST['obj_id']))    # [1, 2, 3, 1, 1]
        # whole page that their currently on will be updated. So, we can see the cart items being populated.
        return redirect("catalog")
    return main_page


def cart(request):
    cart = request.session['cart']
    request.session.set_expiry(0)
    ctx = {'cart': cart, 'cart_size': len(cart), 'cart_items': cartItems(
        cart), 'total_price': priceCart(cart)}
    return render(request, "store/cart.html", ctx)


def checkout(request):
    cart = request.session['cart']
    request.session.set_expiry(0)
    ctx = {'cart': cart, 'cart_size': len(cart), 'cart_items': cartItems(
        cart), 'total_price': priceCart(cart)}
    return render(request, "store/checkout.html", ctx)


def completeOrder(request):
    request.session.set_expiry(0)
    cart = request.session['cart']
    order = Order()
    order.first_name = request.POST['first_name']
    order.last_name = request.POST['last_name']
    order.address = request.POST['address']
    order.city = request.POST['city']
    order.payment_method = request.POST['payment']
    order.payment_data = request.POST['payment_data']
    order.items = getItemsList(cart)

    order.save()
    request.session['cart'] = []

    return render(request, "store/complete_order.html", None)


@login_required
def editOrder(request, pk):
    order = get_object_or_404(Order, id=pk)
    if request.method == "POST":
        order.id = request.POST['id_items']
        order.items = request.POST['items']
        order.first_name = request.POST['first_name']
        order.last_name = request.POST['last_name']
        order.address = request.POST['address']
        order.city = request.POST['city']
        order.payment_method = request.POST['payment_method']
        order.fulfilled = request.POST['fulfilled']

        order.save()
        # print('success')
        return redirect('admin')

    return render(request, 'store/edit-order.html', {'order': order})


@login_required
def deleteOrder(request, pk):
    order = get_object_or_404(Order, id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('admin')

    return render(request, 'store/confirmation_delete.html', {'order': order})


@login_required
def adminDashboard(request):
    orders = Order.objects.all()
    ctx = {'orders': orders}
    return render(request, "store/admin_panel.html", ctx)
