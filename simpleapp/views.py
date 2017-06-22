
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from django.urls import reverse, reverse_lazy

from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView


from django.utils import timezone
from .models import Book

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'lql'

    def get_queryset(self):
        return Book.objects.all()


class DetailView(generic.DetailView):
    model = Book
    template_name = 'detail.html'

    def get_queryset(self):
        return Book.objects.all()

class AddView(CreateView):
    template_name = 'add.html'
    model=Book
    pub_date=timezone.now()
    fields=['title']

class UpdateView(UpdateView):
    template_name = 'books_update_form.html'
    model=Book
    pub_date=timezone.now()
    fields=['car_text']
    template_name_suffix = '_update_form'

class DeleteView(DeleteView):
    template_name = 'book_confirm_delete.html'
    model = Book
    success_url=reverse_lazy('book-list')
