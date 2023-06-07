from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('shop/', include('shop.urls')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
]

if settings.DEBUG is False:  # if DEBUG is True it will be served automatically
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)