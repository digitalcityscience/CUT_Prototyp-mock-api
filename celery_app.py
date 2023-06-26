from celery import Celery

app = Celery('celeryapp')
app.config_from_object('celery_config')

if __name__ == '__main__':
    app.start()