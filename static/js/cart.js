var updateBtn= document.getElementsByClassName('update-cart')

for (var i=0; i < updateBtn.length; i++){
    updateBtn[i].addEventListener('click',function(){
        // get the data in the html elment attrubtes 
        var productId = this.dataset.product;
        var action =  this.dataset.action;

        if(user == 'AnonymousUser'){
            addCookieItem(productId,action)
        }else{
            updateUserOrder(productId,action)
        }
    })
}

// create a cart for unauthenticated user
function addCookieItem(productId,action){

    // Add items to an order
    if(action == 'add'){
        if(cart[productId] ==undefined){
            cart[productId]= {'quantity':1}
        }else{
            cart[productId]['quantity'] += 1;
        }
    }
    // remove products from an order
    if(action == 'remove'){
        cart[productId]['quantity'] -= 1;
        if(cart[productId]['quantity'] <= 0){
            console.log('Product removed')
            delete cart[productId]
        }
    }
    console.log('Cart:', cart)
    document.cookie = 'cart='+JSON.stringify(cart)+";domain=;path=/"
    location.reload()
}

function updateUserOrder(productId, action){
    url ='/addcart/'
    fetch(url,{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'product':productId, 'action':action})
    })
    .then(response=>response.json())
    .then(data=>{
        console.log(data)
        location.reload()
    })
}


