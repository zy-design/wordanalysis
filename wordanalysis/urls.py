"""wordanalysis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))pyt
"""
from django.contrib import admin
from django.conf.urls import include, url
from django.urls import path, re_path
from . import views
from mymain import views as main_views
from django.views.static import serve
from .settings import MEDIA_ROOT

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('hello/', views.hello),
    # url('mymain/', include('mymain.urls')),
    url(r'^$', main_views.index),
    # url('mymain/mymain_index.html', main_views.index),
    url('mymain/search', main_views.search),
    url('mymain/download_file', main_views.download_file),
    url('mymain/download_image', main_views.download_image),
    url('mymain/download', main_views.download),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
]
