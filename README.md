# Omotes celery worker

This is a trial repo to test a celery setup with different worker types with their own code repo.
The application and workers each run in their own container:

```
docker-compose up
```

Worker 'type-a' is run in 10 containers via docker replica's.  
Worker 'type-b' is run with a celery autoscale of 10.

Go to http://localhost:8889/dashboard to view statistics.