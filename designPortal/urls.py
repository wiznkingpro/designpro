# design_portal/urls.py
import os

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from designPortal.settings import BASE_DIR

urlpatterns = [
    path('superadmin/', admin.site.urls),             # ← админка
    path('', include('portal.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'portal/static'),
]