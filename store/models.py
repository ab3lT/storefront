from django.db import models

class Promotion(models.Model):
   description =  models.CharField(max_length = 255)
   discount = models.FloatField()
   
class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Product', on_delete = models.SET_NULL, null = True, related_name= '+')
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['title']
    
class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    #9999/99
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now = True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT, related_name = 'products')
    promotions  = models.ManyToManyField(Promotion)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title']
    
class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P',
    PAYMENT_STATUS_COMPLETE = 'C',
    PAYMENT_STATUS_FAILED = 'F',
    
    PAYMENT_STATUS_CHOICES = [
        ('P', 'Pending'),
        ('C', 'Complete'),
        ('F', 'Failed')
    ]
    placed_at = models.DateTimeField(auto_now_add = True)   
    payment_status = models.CharField(max_length=1, choices = PAYMENT_STATUS_CHOICES, default = PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey('Customer', on_delete = models.PROTECT)

class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'
    
    MEMBERSHIP_CHOICES = [
            ('B', 'Bronze'),
            ('S', 'Silver'),
            ('G', 'Gold')
    ]
    first_name = models.CharField(max_length = 40)
    last_name = models.CharField(max_length = 40)
    email = models.EmailField(unique = True)
    phone = models.CharField(max_length = 12)
    birth_date = models.DateField(null = True)
    membership = models.CharField(max_length=1, choices = MEMBERSHIP_CHOICES, default = MEMBERSHIP_BRONZE)
    
    class Meta:
        db_table = 'store_customer'
        indexes = [
            models.Index(fields = ['first_name', 'last_name'])
        ]
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    class Meta:
        ordering = ['first_name', 'last_name']
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete = models.PROTECT)
    product = models.ForeignKey(Product, on_delete = models.PROTECT, related_name = 'orderitems')
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits= 6, decimal_places = 2)
class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip = models.PositiveSmallIntegerField()
    customer = models.OneToOneField(Customer, on_delete= models.CASCADE, primary_key = True)

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add = True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete= models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    