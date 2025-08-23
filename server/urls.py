<<<<<<< Updated upstream
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/',include("accounts.urls")),
    # path('api/',include("api.urls")),
]
=======
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include("accounts.urls")),
    path('api/',include("api.urls")),
]
>>>>>>> Stashed changes
