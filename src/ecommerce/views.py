from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .forms import ProductModelForm
from .models import ProductModel

from orders.models import Order
from cart.models import Cart
from product.models import Product


# =========================================================
# VISTAS DE PRODUCTOS
# =========================================================

def product_model_delete_view(request, product_id):

    instance = get_object_or_404(
        ProductModel,
        id=product_id
    )

    if request.method == "POST":

        instance.delete()

        messages.success(
            request,
            "Producto eliminado"
        )

        return HttpResponseRedirect("/ecommerce/")

    context = {
        "product": instance
    }

    return render(
        request,
        "ecommerce/delete-view.html",
        context
    )


def product_model_update_view(request, product_id=None):

    instance = get_object_or_404(
        ProductModel,
        id=product_id
    )

    form = ProductModelForm(
        request.POST or None,
        instance=instance
    )

    if form.is_valid():

        instance = form.save(commit=False)

        instance.save()

        messages.success(
            request,
            "Producto actualizado con éxito"
        )

        return HttpResponseRedirect(
            "/ecommerce/{product_id}".format(
                product_id=instance.id
            )
        )

    context = {
        "form": form
    }

    return render(
        request,
        "ecommerce/update-view.html",
        context
    )


def product_model_create_view(request):

    form = ProductModelForm(
        request.POST or None
    )

    if form.is_valid():

        instance = form.save(commit=False)

        instance.save()

        messages.success(
            request,
            "Producto creado con éxito"
        )

        return HttpResponseRedirect(
            "/ecommerce/{product_id}".format(
                product_id=instance.id
            )
        )

    context = {
        "form": form
    }

    return render(
        request,
        "ecommerce/create-view.html",
        context
    )


def product_model_detail_view(request, product_id):

    instance = get_object_or_404(
        ProductModel,
        id=product_id
    )

    context = {
        "product": instance
    }

    return render(
        request,
        "ecommerce/detail-view.html",
        context
    )


def product_model_list_view(request):

    query = request.GET.get(
        "q",
        None
    )

    queryset = ProductModel.objects.all()

    if query is not None:

        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(price__icontains=query)
        )

    context = {
        "products": queryset
    }

    if request.user.is_authenticated:

        template = "ecommerce/list-view.html"

    else:

        template = "ecommerce/list-view-public.html"

    return render(
        request,
        template,
        context
    )


@login_required
def login_required_view(request):

    queryset = ProductModel.objects.all()

    context = {
        "products": queryset
    }

    if request.user.is_authenticated:

        template = "ecommerce/list-view.html"

    else:

        template = "ecommerce/list-view-public.html"

    return render(
        request,
        template,
        context
    )


class ProtectedListView(
    LoginRequiredMixin,
    ListView
):

    model = ProductModel

    template_name = "ecommerce/list-view.html"

    context_object_name = "products"

    def get_queryset(self):

        return ProductModel.objects.filter(
            user=self.request.user
        )


# =========================================================
# VISTAS DE VENTAS
# =========================================================

def ventas_view(request):

    productos = ProductModel.objects.all()

    carrito = request.session.get(
        "carrito",
        []
    )

    context = {
        "productos": productos,
        "carrito": carrito
    }

    return render(
        request,
        "ventas/ventas.html",
        context
    )


# =========================================================
# AGREGAR PRODUCTO AL CARRITO
# =========================================================

def agregar_carrito(request, product_id):

    producto = get_object_or_404(
        ProductModel,
        id=product_id
    )

    carrito = request.session.get(
        "carrito",
        []
    )

    carrito.append({
        "id": producto.id,
        "titulo": producto.title,
        "precio": float(producto.price)
    })

    request.session["carrito"] = carrito

    request.session.modified = True

    messages.success(
        request,
        f"{producto.title} agregado al carrito."
    )

    return redirect("ventas")


# =========================================================
# PROCESAR PEDIDO
# =========================================================

@login_required
def procesar_pedido(request):

    if request.method != "POST":

        return HttpResponse(
            "Método no permitido.",
            status=405
        )

    carrito = request.session.get(
        "carrito",
        []
    )

    # -----------------------------------------------------
    # Verificar carrito
    # -----------------------------------------------------

    if not carrito:

        messages.error(
            request,
            "El carrito está vacío."
        )

        return redirect("ventas")

    # -----------------------------------------------------
    # Crear Cart
    # -----------------------------------------------------

    cart = Cart.objects.create(
        user=request.user
    )

    total = 0

    # -----------------------------------------------------
    # Procesar productos
    # -----------------------------------------------------

    for item in carrito:

        producto_id = item["id"]

        precio = float(
            item["precio"]
        )

        total += precio

        # -------------------------------------------------
        # IMPORTANTE
        #
        # ProductModel y Product son modelos diferentes.
        #
        # Creamos un Product para que Cart.products
        # pueda guardar correctamente la relación.
        # -------------------------------------------------

        producto_ecommerce = Product.objects.create(

            name=item["titulo"],

            description="Producto vendido desde ecommerce",

            price=precio
        )

        cart.products.add(
            producto_ecommerce
        )

    # -----------------------------------------------------
    # Crear Order
    # -----------------------------------------------------

    Order.objects.create(
        cart=cart,
        total=total
    )

    # -----------------------------------------------------
    # Vaciar carrito
    # -----------------------------------------------------

    request.session["carrito"] = []

    request.session.modified = True

    # -----------------------------------------------------
    # Mensaje
    # -----------------------------------------------------

    messages.success(
        request,
        "Pedido realizado correctamente."
    )

    return redirect("ventas")


# =========================================================
# VACIAR CARRITO
# =========================================================

def vaciar_carrito(request):

    request.session["carrito"] = []

    request.session.modified = True

    messages.success(
        request,
        "Carrito vaciado."
    )

    return redirect("ventas")


# =========================================================
# DATOS PARA LA GRÁFICA
# =========================================================

def ventas_data_view(request):

    if request.method != "GET":

        return JsonResponse(
            {
                "error": "Método no permitido."
            },
            status=405
        )

    ventas = Order.objects.all().order_by(
        "created_at"
    )

    labels = []

    data = []

    for venta in ventas:

        labels.append(
            venta.created_at.strftime(
                "%Y-%m-%d"
            )
        )

        data.append(
            float(venta.total)
        )

    return JsonResponse(
        {
            "labels": labels,
            "data": data
        }
    )