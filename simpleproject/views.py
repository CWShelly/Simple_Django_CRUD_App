from django.http import HttpResponse

def root_page(request):
    return HttpResponse("Go to:  http://127.0.0.1:8000/books/")
