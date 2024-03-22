from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer
from django.http import HttpResponse
from django.http import JsonResponse
from Arifpay_Plugin import ArifPay
import requests

arifpay= ArifPay("G8FbER8zZ9uco5tLuVnNKycJwXzvJTyo","2025-02-01T03:45:27")
# Create your views here.

paymentInfo= {
    "cancelUrl": "https://example.com",
    "errorUrl": "http://error.com",
    "notifyUrl": "https://gateway.arifpay.net/test/callback",
    "successUrl": "http://example.com",
    "paymentMethods": [
      "TELEBIRR"
    ],
    "expireDate": "2025-02-01T03:45:27",
    "items": [
        {
            "name": "ሙዝ",
            "quantity": 1,
            "price": 100,
            "description": "Fresh Corner preimuim Banana.",
            "image": "https://4.imimg.com/data4/KK/KK/GLADMIN-/product-8789_bananas_golden-500x500.jpg"
        },
        {
            "name": "ሙዝ",
            "quantity": 1,
            "price": 1,
            "description": "Fresh Corner preimuim Banana.",
            "image": "https://4.imimg.com/data4/KK/KK/GLADMIN-/product-8789_bananas_golden-500x500.jpg"
        }
    ],
    "beneficiaries": [
        {
            "accountNumber": "01320811436100",
            "bank": "Abet",
            "amount": 2.0
        }
    ],
    "lang": "EN"
}

@api_view(['GET'])
def createcheckout(request):
    if request.method=='GET':
        response=arifpay.Make_payment(paymentInfo)
        return JsonResponse(response)
    
@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        queryset = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(queryset, many=True, context = {'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer.validated_data
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
@api_view(['GET', 'PUT'])
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data = request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
 
@api_view() 
def collection_detail(request, pk):
    return Response('ok')