"""simpleproject URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
from simpleproject.views import root_page

#
from rest_framework.urlpatterns import format_suffix_patterns
from books import views
from books.models import Book
#

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', root_page),
    url(r'^books/', include('books.urls', namespace="books")),
    url(r'^listbooks/$', views.BookList.as_view()),
    url(r'^bookdetail/(?P<pk>[0-9]+)/$', views.BookDetail.as_view())
]

urlpatterns=format_suffix_patterns(urlpatterns)
