from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q, F
from store.models import Product
# Create your views here.
# request -> response
# request handler
# action

def hello(request):
    # query_set = Product.objects.filter(unit_price__range=(20,30))
    # query_set = Product.objects.filter(inventory__lt=10, unit_price__lt=20)
    # query_set = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20))
    query_set = Product.objects.filter(inventory= F('unit_price'))
    
    # for product in query_set:
    #     print(product)
    return render(request, 'hello.html', {'name': 'abel', 'products': list(query_set)})