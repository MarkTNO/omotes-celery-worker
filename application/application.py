import threading
import time
import random

from celery import Celery
from celery.result import AsyncResult

first_task = True


def perform_task(t_name, q_name):
    global nr_of_completed_tasks
    global total_delay
    task_to_perform = app.signature(t_name, (nr_of_completed_tasks, 3), queue=q_name).delay()
    global first_task
    if first_task:  # print status of first task only
        first_task = False
        delay = 0
        while delay < 10 and task_to_perform:
            delay += 0.1
            time.sleep(delay)  # print 10 times per second
            print(f"============= TASK PROGRESS: {task_to_perform.info}")

    result_perform = task_to_perform.get()
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
nr_of_completed_tasks = 0
total_delay = {'type-a': 0, 'type-b': 0}

threads = []
for i in range(numTasks):
    if random.randint(0, 1) == 0:
        task_name = 'add-task'
        queue_name = 'type-a'
    else:
        task_name = 'multiply-task'
        queue_name = 'type-b'
    t = threading.Thread(target=perform_task, args=(task_name, queue_name,))
    t.daemon = True
    threads.append(t)
    t.start()

# wait for all tasks to be completed
for thr in threads:
    thr.join()

end = time.time()
print(f"Application ended, completed tasks: {nr_of_completed_tasks}")
print(f"Application execution time: {end - start} seconds")
print(f"Total delay time per worker type: {total_delay}")
