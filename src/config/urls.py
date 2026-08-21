from django.conf import settings
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path(
        "up/",
        include("up.urls")
    ),

    path(
        "",
        include("pages.urls")
    ),

    path(
        "ecommerce/",
        include("ecommerce.urls")
    ),

    path(
        "admin/",
        admin.site.urls
    ),
]


if not settings.TESTING:

    urlpatterns = [
        *urlpatterns,

        path(
            "__debug__/",
            include("debug_toolbar.urls")
        ),
    ]