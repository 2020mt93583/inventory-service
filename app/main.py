import random

from fastapi import FastAPI
from redis_om import get_redis_connection, HashModel

app = FastAPI()

redis = get_redis_connection(
    host="localhost",
    port=6379,
    password="eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81",
    decode_responses=True
)


class Product(HashModel):
    name: str
    price: float
    stock: int

    class Meta:
        database = redis


def create_default_inventory():
    for pk in Product.all_pks():
        if Product.get(pk):
            print("default inventory already exists")
            return
    for i in range(1, 11):
        product = Product(
            name="item" + str(i),
            price=random.randint(a=50, b=100),
            stock=random.randint(a=100, b=200)
        )
        product.save()
    print('Default inventory created')


create_default_inventory()


@app.get('/products')
def get_all():
    return [_format(pk) for pk in Product.all_pks()]


def _format(pk: str):
    product = Product.get(pk)

    return {
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'stock': product.stock
    }


@app.post('/products')
def create(product: Product):
    return product.save()


@app.get('/products/{pk}')
def get(pk: str):
    return Product.get(pk)


@app.delete('/products/{pk}')
def delete(pk: str):
    return Product.delete(pk)
