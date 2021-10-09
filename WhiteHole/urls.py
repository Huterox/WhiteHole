"""WhiteHole URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from BASEAPP import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    url(r'^admin/', admin.site.urls,name="admin"),
    url(r'^Base/',include(("BASEAPP.urls","Base"),namespace="Base")),
    url(r"^Blog/",include(("Blog.urls","Blog"),namespace="Blog")),
    url(r"^Channel/",include(("Channel.urls","Channel"),namespace="Channel")),
    path(r"",views.index,name="index"),
    url(r'mdeditor/', include('mdeditor.urls')),

]

if settings.DEBUG:
    # static files (images, css, javascript, etc.)主要是让页面显示正常
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


