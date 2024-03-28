from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .models import Collection, Product
from .serializers import CollectionSerializer, ProductSerializer
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models.aggregates import Count
from rest_framework.mixins import ListModelMixin, CreateModelMixin
class ProductList(APIView):

    def get(self, request):
        queryset = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(queryset, many=True, context = {'request': request})
        return Response(serializer.data)
    """
        Endpoint Test Description
        
        ---
        request_serializer: YourSerializer
        response_serializer: YourResponseSerializer
        
        parameters:
        - name: required_field
          description: Description of the required field
          required: true
          type: string
        - name: optional_field
          description: Description of the optional field
          required: false
          type: string
          
        """
    def post(self, request):
        serializer = ProductSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer.validated_data
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'

    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        if product.orderitems.count() > 0:
            return Response({'error': 'product cannot be deleted because it is associated with an order item '},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class CollectionList(APIView):
    def get(self, request):
        queryset = Collection.objects.annotate(products_count=Count('products')).all()
        serializer = CollectionSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CollectionDetail(RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.annotate(
        products_count = Count('products'))
    serializer_class = CollectionSerializer
    lookup_field = 'id'
    
    
    def delete(self, request,id):
        collection = get_object_or_404(
        Collection.objects.annotate(
        products_count = Count('products')), pk=id)
        if collection.products.count() > 0 :
            return Response({'error': 'collection cannot be deleted because it includes one or more products '},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        




 