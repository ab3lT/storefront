from typing import Any
from django.db.models.aggregates import Count
from django.contrib import admin, messages
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models


class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low')
        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)

    
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    prepopulated_fields ={
        'slug': ['title']
    }
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_title']
    actions = ['clear_inventory']
    list_editable = ['unit_price']
    list_filter = ['collection', 'last_update', InventoryFilter]
    list_per_page = 10
    list_select_related = ['collection']
    def collection_title(self, product):
        return product.collection.title
    
    admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'Ok'
    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were successfully updated.',
            messages.ERROR
        )

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name',  'phone', 'membership', 'orders']
    list_editable = ['membership']
    list_per_page = 10
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
    @admin.display(ordering='orders_count')
    def orders(self, customer):
        url = (
            reverse('admin:store_order_changelist')
            + '?'
            + urlencode({
                'customer__id': str(customer.id)
            }))
        return format_html('<a href="{}">{} Orders</a>', url, customer.orders_count)
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders_count=Count('order')
        )
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    # autocomplete_fields = ['featured_product']
    search_fields = ['title']
    list_display = ['title', 'product_count']
    
    @admin.display(ordering='product_count')
    def product_count(self, collection):
        url = (
            reverse('admin:store_product_changelist')
            + '?'
            + urlencode({
                'collection__id': str(collection.id)
            }))
        return format_html('<a href="{}">{} Products</a>', url, collection.product_count)
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(
                            product_count= Count('products')
                            )

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    list_display = ['id', 'placed_at', 'payment_status', 'customer']
    list_select_related = ['customer']
    list_per_page = 10
    
    # def customer_information(self, Order):
    #     return 'Full-Name: ' + Order.customer.first_name + ' ' + Order.customer.last_name + ' Phone-Number:  ' + Order.customer.phone