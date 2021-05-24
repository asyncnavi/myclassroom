from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from .view import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name="home"),
    path('auth/', include('authentications.urls')),
    path('class/', include('classes.urls'))
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
