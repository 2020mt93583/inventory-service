from main import Product
from redis_om import get_redis_connection, HashModel

import os
import time

key = 'order_completed'
group = 'inventory-group'

eventq = get_redis_connection(
    host=os.environ['eventq-host-name'],
    port=6379,
    password=os.environ['eventq-pass'],
    decode_responses=True
)

try:
    eventq.xgroup_create(key, group)
except:
    print('Group already exists!')

while True:
    try:
        results = eventq.xreadgroup(group, key, {key: '>'}, None)

        if results:
            for result in results:
                obj = result[1][0][1]
                try:
                    product = Product.get(obj['product_id'])
                    product.stock = product.stock - int(obj['quantity'])
                    product.save()
                except:
                    eventq.xadd('refund_order', obj, '*')

    except Exception as e:
        print(str(e))
    time.sleep(1)