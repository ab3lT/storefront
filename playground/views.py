from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
# request -> response
# request handler
# action

def hello(request):
    x = 1
    y = 2
    # return HttpResponse("Hello world")
    return render(request, 'hello.html', {'name': 'abel'})