from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .forms import ProductModelForm
from .models import ProductModel


# Create your views here.

def product_model_delete_view(request, product_id):
    instance = get_object_or_404(ProductModel, id=product_id)

    if request.method == "POST":
        instance.delete()
        messages.success(request, "Producto eliminado")
        return HttpResponseRedirect("/ecommerce/")

    context = {
        "product": instance
    }

    template = "ecommerce/delete-view.html"
    return render(request, template, context)


def product_model_update_view(request, product_id=None):
    instance = get_object_or_404(ProductModel, id=product_id)

    form = ProductModelForm(request.POST or None, instance=instance)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Producto actualizado con éxito")
        return HttpResponseRedirect(
            "/ecommerce/{product_id}".format(product_id=instance.id)
        )

    context = {
        "form": form
    }

    template = "ecommerce/update-view.html"
    return render(request, template, context)


def product_model_create_view(request):
    form = ProductModelForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Producto creado con éxito")
        return HttpResponseRedirect(
            "/ecommerce/{product_id}".format(product_id=instance.id)
        )

    context = {
        "form": form
    }

    template = "ecommerce/create-view.html"
    return render(request, template, context)


def product_model_detail_view(request, product_id):
    instance = get_object_or_404(ProductModel, id=product_id)

    context = {
        "product": instance
    }

    template = "ecommerce/detail-view.html"

    return render(request, template, context)


def product_model_list_view(request):
    query = request.GET.get("q", None)

    queryset = ProductModel.objects.all()

    if query is not None:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(price__icontains=query)
        )

    template = "ecommerce/list-view.html"

    context = {
        "products": queryset
    }

    if request.user.is_authenticated:
        template = "ecommerce/list-view.html"
    else:
        template = "ecommerce/list-view-public.html"

    return render(request, template, context)


@login_required
def login_required_view(request):

    print(request.user)

    queryset = ProductModel.objects.all()

    template = "ecommerce/list-view.html"

    context = {
        "products": queryset
    }

    if request.user.is_authenticated:
        template = "ecommerce/list-view.html"
    else:
        template = "ecommerce/list-view-public.html"

    return render(request, template, context)



# NUEVA VISTA PARA LA ACTIVIDAD
class ProtectedListView(LoginRequiredMixin, ListView):

    model = ProductModel
    template_name = "ecommerce/list-view.html"
    context_object_name = "products"

    def get_queryset(self):
        return ProductModel.objects.filter(user=self.request.user)