import time
import random

from celery import Celery

app = Celery(
    'omotes',
    broker='amqp://user:bitnami@rabbitmq',
    backend='rpc://user:bitnami@rabbitmq',
    broker_connection_retry_on_startup=True
)


@app.task(name='add-task', bind=True)  # Named task
def add(self, x, y):
    print('Task Add started')
    delay = 10 * random.random()
    for step in range(5):
        time.sleep(delay / 5)  # Simulate a long task
        self.update_state(state='PROGRESS', meta={'progress': step / 4})
    print('Task Add done')
    return delay
