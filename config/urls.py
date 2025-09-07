"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from notifications.admin_site import custom_admin_site

from accounts import admin_registry
from home import admin_registry
from notifications import admin_registry
from article import admin_registry



handler403 = 'accounts.views.custom_permission_denied_view'
# handler404 = 'accounts.views.custom_permission_denied'

urlpatterns = [
        path("admin/", custom_admin_site.urls),
        path('',include('home.urls')),
        path('accounts/', include('accounts.urls')),
        path('article/', include('article.urls')),

        # Rosetta (i18n)
        path('rosetta/',include('rosetta.urls')),

        # CKEditor
        path("ckeditor/", include("ckeditor_uploader.urls")),

]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


