"""
URL configuration for somesite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from django.contrib.sitemaps.views import sitemap
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings
from django.contrib import admin

from .sitemaps import sitemaps

urlpatterns = []

urlpatterns += i18n_patterns(
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    
    path('req/', include('requestdataapp.urls')),
    path('shop/', include('shopapp.urls')),
    path('accounts/', include('myauthapp.urls')),
    path('blog/', include('BlogApp.urls')),
    
    path('api/', include('myapiapp.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name ='schema'),
    path('api/schema/swagger/', SpectacularSwaggerView.as_view(url_name = 'schema'), name ='swagger'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name = 'schema'), name = 'redoc'),
    
    path('sitemap.xml',
        sitemap,
        {'sitemaps':sitemaps}, 
        name = 'django.contrib.sitemaps.views.sitemap'
        ),
    )

if settings.DEBUG:
    urlpatterns.extend(
        static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    )
    urlpatterns.append(
        path('__debug__/', include('debug_toolbar.urls')),
    )