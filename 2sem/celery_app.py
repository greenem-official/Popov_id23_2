from celery import Celery

# app = Celery(
#     'tasks',
#     broker='redis://localhost:6379/0',
#     backend='redis://localhost:6379/1',
#     include=['app.CeleryTasks']
# )

app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/1',
    include=['app.CeleryTasks'],
    worker_pool='solo',
)

app.conf.update(
    include=['app.CeleryTasks'],
    task_serializer='json',
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_time_limit=300,
)
