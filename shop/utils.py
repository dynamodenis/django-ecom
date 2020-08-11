import json
from .models import *


# for UNAUTHENTICATED USER
def cartCookie(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    
    
    items=[]
    order={'get_order_total':0,'get_order_price':0.00, 'shipping':False}
    cartitems = order['get_order_total']
    
    # add each quantity tn the cart to the tems
    for i in cart:
        # Get the item if its present in the database
        try:
            cartitems += cart[i]['quantity']
            # set the product using id and set the total price and total quantity
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])
            
            order['get_order_total'] += cart[i]['quantity']
            order['get_order_price'] += float(total)
            
            item = {
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'image':product.image
                },
                'quantity':cart[i]['quantity'],
                'get_total':total,
            }
            items.append(item)
            
            if product.digital == False:
                order['shipping']=True
        except:
            pass
    return {'items':items,'order':order,'cartitems':cartitems}


# combine the authnticated user logic with with cartCookie()
def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created= Order.objects.get_or_create(customer=customer, complete = False)
        items=order.orderitem_set.all()
        cartitems = order.get_order_total
        
    else:
        # ##--------------------------------The commented code is to avoid repetion in all the views so we declare ot as a fucntion in tha utils.py as cartCookie then import it-----------------------
        cookieData = cartCookie(request)
        items = cookieData['items']
        order = cookieData['order']
        cartitems = cookieData['cartitems']
    return {'items':items,'order':order,'cartitems':cartitems}


def get0rder(request,data):
    # get user name and email form the form object
    name = data['form']['name']
    email = data['form']['email']
    
    # use cookieCart to get the passed in items
    cookieData = cartCookie(request)
    items = cookieData['items']
    
    # create a a customer instance for the not signed in user
    customer, created =Customer.objects.get_or_create(
        email = email
    )
    customer.name = name
    customer.save()
    
    # create the order with this customer
    order = Order.objects.create(customer=customer,complete = False)
    
    # user item to create an orderItems
    for item in items:
        # get the product using the set product id from cookiCart()
        product = Product.objects.create(id=item['product']['id'])
        
        # create orderitem
        orderitem = OrderItem.objects.create(
            product = product,
            order = order,
            quantity = item['quantity']
        )
    return customer, order
