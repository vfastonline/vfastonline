"""vfast URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from vfast import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^logout', views.logout),
    url('^u/', include('vuser.urls')),
    url('^head/', include('vgrade.urls')),
    url('^course/', include('vcourse.urls')),
    url('^r/', include('vrecord.urls')),
    url('^badge/', include('vbadge.urls')),
    url('^test', views.test),
    url('^search', views.search, name='search'),
    url('^navtabs', views.search_js, name='navtabs'),
    url('^dashBoard', views.dashBoard),
    url('^video/(\d+)/$', views.playVideo),
    url('^practice/(\d+)/$', views.practice,),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

