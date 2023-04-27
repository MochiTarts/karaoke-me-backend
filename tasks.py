from celery import Celery, Task

def make_celery(app):
  class FlaskTask(Task):
    def __call__(self, *args, **kwargs):
      with app.app_context():
        return Task.__call__(self, *args, **kwargs)
      
  celery = Celery(app.name, task_cls=FlaskTask)
  celery.config_from_object(app.config['CELERY'])
  celery.set_default()
  app.extensions['celery'] = celery
  return celery