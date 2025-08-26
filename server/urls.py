from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/',include("accounts.urls")),
    path('api/',include("api.urls")),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger schema view
schema_view = get_schema_view(
   openapi.Info(
      title="API барои Flutter",
      default_version='v1',
      description="Ин Swagger API мебошад барои пайвастшавӣ бо Flutter",
      contact=openapi.Contact(email="example@email.com"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # Шумо метавонед номи app-атро иваз кунӣ
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

