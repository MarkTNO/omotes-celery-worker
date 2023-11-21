import threading
import time
import random

from celery import Celery

task_nr = 0


def perform_task(t_name, q_name):
    task_to_perform = app.signature(task_name, (i, 3), queue=queue_name).delay()
    result_perform = task_to_perform.get()
    global nr_of_completed_tasks
    global total_delay
    nr_of_completed_tasks += 1
    total_delay[q_name] += result_perform
    print(f"Received result: '{result_perform}' from task nr: {nr_of_completed_tasks}, from queue: {q_name}")


print('Application started')

app = Celery(
    'omotes',
    broker='amqp://user:bitnami@rabbitmq',
    backend='rpc://user:bitnami@rabbitmq',
)

start = time.time()
numTasks = 100
tasks_dict = {'type-a': [], 'type-b': []}

threads = []
for i in range(numTasks):
    if random.randint(0, 1) == 0:
        task_name = 'addTask'
        queue_name = 'type-a'
    else:
        task_name = 'multiplyTask'
        queue_name = 'type-b'
    t = threading.Thread(target=perform_task, args=(task_name, queue_name,))
    t.daemon = True
    threads.append(t)
    t.start()

nr_of_completed_tasks = 0
total_delay = {'type-a': 0, 'type-b': 0}

for thr in threads:
    thr.join()

end = time.time()
print(f"Application ended, completed tasks: {nr_of_completed_tasks}")
print(f"Application execution time: {end - start} seconds")
print(f"Total delay time per worker type: {total_delay}")