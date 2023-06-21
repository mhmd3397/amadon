from django.shortcuts import render, redirect
from .models import Order, Product


def index(request):
    context = {
        "all_products": Product.objects.all()
    }
    return render(request, "store/index.html", context)


def checkout(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        quantity_from_form = int(request.POST.get("quantity", 0))
        product = Product.objects.get(id=product_id)
        total_charge = product.price * quantity_from_form
        print("Charging credit card...")
        Order.objects.create(
            quantity_ordered=quantity_from_form,
            total_price=total_charge)
        return redirect("checkout-success")
    else:
        return redirect("index")


def checkout_success(request):
    orders = Order.objects.all()
    total_items_ordered = orders.count()
    total_amount_charged = sum(order.total_price for order in orders)
    context = {
        "total_items_ordered": total_items_ordered,
        "total_amount_charged": total_amount_charged,
    }
    return render(request, "store/checkout.html", context)
