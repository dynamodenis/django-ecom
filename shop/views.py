from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
from .utils import cartCookie,cartData,get0rder

# Create your views here.
def index(request):
    products = Product.objects.order_by('name')
    # THIS WILL BE DELTED IT GETS THE TOTAL CART ITEMS
    # Now u can acces the cartData function from utils which hold the logic for both authenticated and unaunthenticated users
    
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartitems = data['cartitems']
            
    return render(request,'index.html',{'products':products,'cartitems':cartitems})

# Cart
def cart(request):
    # Now u can acces the cartData function from utils which hold the logic for both authenticated and unaunthenticated users
    
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartitems = data['cartitems']
        
        
        # try:
        #     cart = json.loads(request.COOKIES['cart'])
        # except:
        #     cart = {}
        # print(cart)
        # items=[]
        # order={'get_order_total':0,'get_order_price':0.00, 'shipping':False}
        # cartitems = order['get_order_total']
        
        # # add each quantity tn the cart to the tems
        # for i in cart:
        #     try:
        #         cartitems += cart[i]['quantity']
        #         # set the product using id and set the total price and total quantity
        #         product = Product.objects.get(id=i)
        #         total = (product.price * cart[i]['quantity'])
                
        #         order['get_order_total'] += cart[i]['quantity']
        #         order['get_order_price'] += float(total)
                
        #         item = {
        #             'product':{
        #                 'id':product.id,
        #                 'name':product.name,
        #                 'price':product.price,
        #                 'image':product.image
        #             },
        #             'quantity':cart[i]['quantity'],
        #             'get_total':total,
        #         }
        #         items.append(item)
                
        #         if product.digital == False:
        #             order['shipping']=True
        #     except:
        #         pass
            
            
    return render(request,'cart.html',{'items':items,'order':order,'cartitems':cartitems})

# checkout
def checkout(request):
    # Now u can acces the cartData function from utils which hold the logic for both authenticated and unaunthenticated users
    
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartitems = data['cartitems']
    return render(request,'checkout.html',{'items':items,'order':order,'cartitems':cartitems})

def updateCart(request):
    data = json.loads(request.body)
    productId=data['product']
    action = data['action']
    
    customer=request.user.customer
    # query the order by the user
    order,create = Order.objects.get_or_create(customer=customer,complete=False)
    # query the orderItem by order and product
    product = Product.objects.get(id=productId)
    orderItem, create = OrderItem.objects.get_or_create(order=order, product=product)
    
    # add the quantity if action is add
    if action == 'add':
        orderItem.quantity=(orderItem.quantity + 1);
        
    elif action == 'remove':
        orderItem.quantity=(orderItem.quantity - 1);
    # save the item   
    orderItem.save()
    
    if orderItem.quantity <= 0:
        orderItem.delete()
    
    return JsonResponse('Item added', safe=False)


def processOrder(request):
    transaction_id=datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        customer=request.user.customer
        # query the order by the user
        order,create = Order.objects.get_or_create(customer=customer,complete=False)
        
        
    else:
        customer,order = get0rder(request,data)
        # # get user name and email form the form object
        # name = data['form']['name']
        # email = data['form']['email']
        
        # # use cookieCart to get the passed in items
        # cookieData = cartCookie(request)
        # items = cookieData['items']
        
        # # create a a customer instance for the not signed in user
        # customer, created =Customer.objects.get_or_create(
        #     email = email
        # )
        # customer.name = name
        # customer.save()
        
        # # create the order with this customer
        # order = Order.objects.create(customer=customer,complete = False)
        
        # # user item to create an orderItems
        # for item in items:
        #     # get the product using the set product id from cookiCart()
        #     product = Product.objects.create(id=item['product']['id'])
            
        #     # create orderitem
        #     orderitem = OrderItem.objects.create(
        #         product = product,
        #         order = order,
        #         quantity = item['quantity']
        #     )
        
    # query the orderItem by order and product
    total = float(data['form']['total'])
    print(total)
    order.transaction_id=transaction_id
    # check if the total send in the frontend is same as the one in the backend
    if total == order.get_order_price:
        order.complete=True
    
    order.save()
    
    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )     
        
        
    return JsonResponse('Order Confirmed', safe=False)