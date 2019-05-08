"""radio4all URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers
from .views import FilesViewSet, LocationViewSet, ProgramsViewSet, HomePageView, AboutPageView, ContactPageView, NewsPageView, FaqPageView, ProgramView, DashboardView, download, filter_type, filter_license, filter_popular
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'files', FilesViewSet)
router.register(r'location', LocationViewSet)
router.register(r'programs', ProgramsViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns = [
    path('',HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('contact/', ContactPageView.as_view(), name='contact'),
    path('news/', NewsPageView.as_view(), name='news'),
    path('program/<int:pk>', ProgramView.as_view(), name='program-detail'),
    path('program/my/', DashboardView.as_view(), name='my-programs'),
    path('faq/', FaqPageView.as_view(), name='faq'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('download/<int:program>/<int:version>/<int:file>/', download),
    path('filter/type/<int:pk>', filter_type),
    path('filter/license/<slug:abbrev>', filter_license),
    path('filter/popular/', filter_popular),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

from django.conf import settings
from django.urls import include, path  # For django versions from 2.0 and up

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)