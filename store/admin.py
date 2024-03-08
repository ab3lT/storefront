from django.contrib import admin
from . import models

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_per_page = 10
    list_select_related = ['collection']
    def collection_title(self, product):
        return product.collection.title
    
    admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'Ok'

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone', 'membership']
    list_editable = ['membership']
    list_per_page = 10
    

admin.site.register(models.Collection)

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'payment_status', 'customer']
    list_select_related = ['customer']
    list_per_page = 10
    
    # def customer_information(self, Order):
    #     return 'Full-Name: ' + Order.customer.first_name + ' ' + Order.customer.last_name + ' Phone-Number:  ' + Order.customer.phone