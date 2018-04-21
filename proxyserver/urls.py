"""proxyserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url
from proxyserver.settings import URLS
from proxyserver.views import Proxy, AuthProxy

urlpatterns = [
    url(r'^admin/(?P<path>.*)', Proxy.as_view(upstream=URLS['webfront'] + 'admin/')),
    url(r'^home/$', Proxy.as_view(upstream=URLS['webfront'] + 'home/')),
    url(r'^login/$', Proxy.as_view(upstream=URLS['webfront'] + 'login/')),
    url(r'^signup/$', Proxy.as_view(upstream=URLS['webfront'] + 'signup/')),
    url(r'^reset_password/(?P<path>.*)', Proxy.as_view(upstream=URLS['webfront'] + 'reset_password/')),
    # url(r'^(?P<path>.*)$', Proxy.as_view(upstream=URLS['webfront'])),
    url(r'^api/v1/(?P<path>.*)', AuthProxy.as_view(upstream='http://taskservice:8000/api/v1/')),
    # url(r'^api/v1/(?P<path>.*)', AuthProxy.as_view()),
    # url(r'^api/(?P<path>.*)', AuthProxy.as_view(upstream='http://authserver:8000/')),
]
