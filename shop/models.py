from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, blank=True , null=True)
    name=models.CharField(max_length=200,null=True)
    email=models.CharField(max_length=200,null=True)
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name=models.CharField(max_length=50, blank=True)
    price=models.DecimalField(max_digits=9, decimal_places=2)
    image = models.ImageField(default='placeholder.png', upload_to='products/')
    digital=models.BooleanField(default=False,blank=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        
        if img.height>300 and img.width>300:
            size=(200,200)
            img.thumbnail(size)
            img.save(self.image.path)
    
class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL, null=True)
    complete=models.BooleanField(default=False)
    date_ordered=models.DateTimeField(auto_now_add=True)
    transaction_id=models.CharField(max_length=50)
    
    def __str__(self):
        return str(self.id)
    # get shipping
    @property
    def shipping(self):
        shipping=False
        
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital==False:
                shipping = True
                
        return shipping
    
    
    # gets total price
    @property
    def get_order_price(self):
        totalitems= self.orderitem_set.all()
        total = sum([item.get_total for item in totalitems])
        return total
    
    @property
    def get_order_total(self):
        totalitems= self.orderitem_set.all()
        total = sum([item.quantity for item in totalitems])
        return total
    
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order =  models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.product.name
    
    @property
    def get_total(self):
        total = self.quantity * self.product.price
        return total
    
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL , null=True)
    address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zipcode = models.CharField(max_length=100, blank=True)
    date_added= models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.address