from django.urls import path
from . import views
from .views import createcheckout


#url conf module
urlpatterns = [
    path('products/', views.product_list),
    path('arifpay/', views.createcheckout),
    path('products/<int:id>/', views.product_detail),
    path('collection/<int:pk>/', views.collection_detail, name = 'collection-detail')
]
