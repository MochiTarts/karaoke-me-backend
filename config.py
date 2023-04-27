import os
from dotenv import load_dotenv
from urllib.parse import quote_plus, urlencode

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()

class Config:
  SECRET_KEY = os.environ.get('APP_SECRET_KEY')
  SQLALCHEMY_DATABASE_URI = f'postgresql://{os.environ.get("POSTGRES_USER")}:{quote_plus(os.environ.get("POSTGRES_PASSWORD"))}@{os.environ.get("DB_HOST")}/{os.environ.get("DB_NAME")}'
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
  AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET")
  AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
  if not int(os.environ.get("PROD")):
    CELERY=dict(
      broker_url=os.environ.get("CELERY_BROKER_URL_DEV", "redis://localhost:6379"),
      result_backend=os.environ.get("CELERY_RESULT_BACKEND_DEV", "redis://localhost:6379"),
      task_ignore_result=True,
    )
    CLIENT_URL="http://localhost:3000"
  else:
    CELERY=dict(
      broker_url=os.environ.get("CELERY_BROKER_URL_PROD", "redis://localhost:6379"),
      result_backend=os.environ.get("CELERY_RESULT_BACKEND_PROD", "redis://localhost:6379"),
      task_ignore_result=True,
    )
    CLIENT_URL="https://karaoke-me.netlify.app"