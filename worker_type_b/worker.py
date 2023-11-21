import time
import random

from celery import Celery

app = Celery(
    'omotes',
    broker='amqp://user:bitnami@rabbitmq',
    backend='rpc://user:bitnami@rabbitmq',
    broker_connection_retry_on_startup = True
)


@app.task(name='multiplyTask')  # Named task
def add(x, y):
    print('Task Multiply started')
    delay = 10 * random.random()
    time.sleep(delay)  # Simulate a long task
    print('Task Multiply done')
    return delay
