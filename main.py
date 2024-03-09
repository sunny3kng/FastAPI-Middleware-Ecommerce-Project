from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from middleware import ecommerce_middleware
from fastapi import HTTPException, Depends
from routers.customer import customers
from routers.product import products
from routers.order import orders
from routers.customer import customer_router
from routers.product import product_router
from routers.order import order_router
from logger import logger

app = FastAPI()
logger.info("starting app")

app.add_middleware(BaseHTTPMiddleware, dispatch=ecommerce_middleware)

app.include_router(customer_router, prefix='/customers', tags=['Customer'])
app.include_router(product_router, prefix='/products', tags=['Product'])
app.include_router(order_router, prefix='/orders', tags=['Order'])

users = [
    {
        'name': 'john',
        'age': 12,
        'phone': '0999900000'
    },
    {
        'name': 'james',
        'age': 12,
        'phone': '0999900000'
    },
    {
        'name': 'janet',
        'age': 12,
        'phone': '0999900000'
    }
]


@app.get('/welcome')
def index():
    return {'message': 'Welcome to our store'}

@app.get('/users')
def get_users():
    return {'message': 'success', 'data': users}

@app.post('/users')
def create_user(name, age, phone):
    user = {
        'name': name,
        'age': age,
        'phone': phone
    }
    users.append(user)
    return {'message': 'User created successfully', 'data': user}

@app.put('/users/{name}')
def update_user(name, age, phone):
    for user in users:
        if user.get('name') == name:
            user['age'] = age
            user['phone'] = phone
            break
    return {'message': 'User updated successfully', 'data': user}

def check_unique_username(username: str):
    if any(customer['name'] == username for customer in customers):
        raise HTTPException(status_code=400, detail="Username already exists")
    return username

@app.put('/users/{username}')
def edit_customer(username: str, age: int, phone: str):
    for user in users:
        if user['name'] == username:
            user['age'] = age
            user['phone'] = phone
            return {'message': 'Customer updated successfully', 'data': user}
    raise HTTPException(status_code=404, detail="Customer not found")

@app.put('/products/{name}')
def edit_product(name: str, price: float):
    for product in products:
        if product['name'] == name:
            product['price'] = price
            return {'message': 'Product updated successfully', 'data': product}
    raise HTTPException(status_code=404, detail="Product not found")

@app.put('/orders/{customer_username}')
def checkout_order(customer_username: str):
    for order in orders:
        if order['customer_username'] == customer_username:
            order['status'] = 'completed'
            return {'message': 'Order checked out successfully', 'data': order}
    raise HTTPException(status_code=404, detail="Order not found")

# GET
# POST
# PUT
# DELETE