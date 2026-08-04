from django.urls import path

from ecommerce import views

urlpatterns = [
    path("", views.product_model_list_view, name="list"),
    path("<int:product_id>", views.product_model_detail_view, name="detail"),
    path("create", views.product_model_create_view, name="create"),
    path("<int:product_id>/edit/", views.product_model_update_view, name="update"),
    path("<int:product_id>/delete/", views.product_model_delete_view, name="delete"),
    path("my-products/", views.ProtectedListView.as_view(), name="my-products"),

    # Nuevas rutas de ventas
    path("ventas/", views.ventas_view, name="ventas"),
    path("ventas/agregar/<int:product_id>/", views.agregar_carrito, name="agregar_carrito"),
    path("ventas/procesar/", views.procesar_pedido, name="procesar_pedido"),
    path("ventas/vaciar/", views.vaciar_carrito, name="vaciar_carrito"),
]