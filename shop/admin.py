from django.contrib import admin
from .models import Customer,Order,OrderItem,Product,ShippingAddress

# change the name of the display name in admin
admin.site.site_title='DynamoShop'
admin.site.site_header='DynamoShop'
admin.site.site_url='DynamoShop'

# Register your models here.
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
