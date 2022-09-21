from django.contrib import admin
from django.urls import path,include
from .settings import MEDIA_URL, MEDIA_ROOT
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
]
urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT) # The Root of saved media files