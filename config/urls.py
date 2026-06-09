from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    #users endpoint
    path('api/users/', include('apps.users.urls')),
    
    #products endpoint
    path('api/products/', include('apps.products.urls'))
    
    #orders endpoint
    path('api/orders/', include('appps.orders.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)