from django.conf.urls import url
from . import views

from .models import Book

app_name="simpleapp"

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name="index"),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name="detail"),
    url(r'^add', views.AddView.as_view(model=Book, success_url='/books'), name="add"),
    url(r'^(?P<pk>[0-9]+)/books_update_form/$', views.UpdateView.as_view(model=Book, success_url='/books'), name='books_update_form'),
        url(r'^(?P<pk>[0-9]+)/book_confirm_delete/$', views.DeleteView.as_view(model=Book, success_url='/books'), name='book_confirm_delete'),
]
