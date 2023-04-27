import os
from config import Config
from flask import Flask
from application.routers import auth, karaoke, youtube_dl
from flask_cors import CORS
from application.tasks import make_celery
from authlib.integrations.flask_client import OAuth
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app():
  app = Flask(__name__)
  app.config.from_object(Config)
  db.init_app(app)

  origins = []
  if int(os.environ.get('PROD')) == 0:
    print("Running in dev mode...")
    origins = ["http://localhost:3000"]
  else:
    origins = ["https://karaoke-me.netlify.app"] # Change once I get an actual production url
  CORS(app, origins=origins, supports_credentials=True)
  
  oauth = OAuth(app)
  oauth.register(
    "auth0",
    client_id=app.config["AUTH0_CLIENT_ID"],
    client_secret=app.config["AUTH0_CLIENT_SECRET"],
    client_kwargs={
      "scope": "openid profile email",
    },
    server_metadata_url=f'https://{app.config["AUTH0_DOMAIN"]}/.well-known/openid-configuration'
  )

  celery = make_celery(app)
  celery.conf.update(app.config)

  with app.app_context():
    from application.models import karaokeinfo
    db.create_all()

  app.register_blueprint(auth.auth_router)
  app.register_blueprint(karaoke.karaoke_router)
  app.register_blueprint(youtube_dl.youtube_dl_router)
  
  return (app, oauth, celery)