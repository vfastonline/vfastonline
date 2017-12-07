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
from oauth.views import github_auth, github_login
from vpractice.views import add_question, question_detail, replay_detail

urlpatterns = [
    url('^github_auth$', github_auth, name='github_auth'),
    url('^github_login/$', github_login, name='github_login'),

    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^project$', views.project),
    url(r'^logout', views.logout),
    url(r'^upload', views.upload, name='upload'),
    url('^u/', include('vuser.urls')),
    url('^course/', include('vcourse.urls')),
    url('^r/', include('vrecord.urls')),
    url('^community/', include('vpractice.urls')),
    url('^info/', include('vinform.urls')),
    url('^badge/', include('vbadge.urls')),
    url('^inspect/', include('vinspect.urls')),
    url('^test', views.test),
    url('^search', views.search_course, name='search'),
    url('^navtabs', views.search_js, name='navtabs'),
    url('^video/(\d+)/$', views.playVideo),
    url('^practice/(\d+)/$', views.practice, ),

    url('^add_question$', add_question, name='add_question'),
    url(r'^question$', question_detail, name='question_detail'),
    url(r'^replay$', replay_detail, name='replay_detail'),
<<<<<<< HEAD
    url(r'^live$', views.live),
    url(r'^interviewlib', views.enterprise_questions),
=======
    url('^resume/', include('vresume.urls')),
>>>>>>> duminchao
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
