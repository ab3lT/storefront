from django.urls import path
from . import views


#url conf module
urlpatterns = [
    path('products/', views.product_list),
    path('products/<int:id>/', views.product_detail),
    path('collection/', views.collection_list),
    path('collection/<int:id>/', views.collection_detail),
    path('collection/<int:pk>/', views.collection_detail, name = 'collection-detail')
]
