from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
# request -> response
# request handler
# action

def hello(request):
    # return HttpResponse("Hello world")
    return render(request, 'hello.html', {'name': 'abel'})