from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BookSerializer

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils import timezone
from .models import Book


class BookList(APIView):

    def get_object(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404

    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class BookDetail(APIView):

    def get_object(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404
    def get(self, request, pk):
        book = self.get_object(pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        book = self.get_object(pk)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk, format=None):
        book = self.get_object(pk)
        print(book)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Create your views here.
class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'latest_question_list'

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
    fields=['title', 'author']

class UpdateView(UpdateView):
    template_name = 'books_update_form.html'
    model=Book
    pub_date=timezone.now()
    fields=['title', 'author']
    template_name_suffix = '_update_form'

class DeleteView(DeleteView):
    template_name = 'book_confirm_delete.html'
    model = Book
    success_url=reverse_lazy('book-list')
