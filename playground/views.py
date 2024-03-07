from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product
# Create your views here.
# request -> response
# request handler
# action

def hello(request):
    query_set = Product.objects.filter(unit_price__range=(20,30))
    
    # for product in query_set:
    #     print(product)
    return render(request, 'hello.html', {'name': 'abel', 'products': list(query_set)})