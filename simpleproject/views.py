from django.http import HttpResponse

def root_page(request):
    return HttpResponse("The Root home page for Simple Project")
