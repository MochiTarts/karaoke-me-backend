import os, json
from dotenv import load_dotenv
from flask import Flask, session, redirect, url_for, after_this_request, jsonify, request
import routers.auth as auth
from routers import karaoke, youtube_dl
from flask_cors import CORS
from dotenv import load_dotenv
from tasks import make_celery
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth

load_dotenv()
app = Flask(__name__)
app.secret_key = os.environ.get("APP_SECRET_KEY")
origins = []
if int(os.environ.get('PROD')) == 0:
  print("Running in dev mode...")
  origins = ["http://localhost:3000"]
  app.config.update(
    CELERY=dict(
      broker_url=os.environ.get("CELERY_BROKER_URL_DEV", "redis://localhost:6379"),
      result_backend=os.environ.get("CELERY_RESULT_BACKEND_DEV", "redis://localhost:6379"),
      task_ignore_result=True,
    ),
    CLIENT_URL="http://localhost:3000"
  )
else:
  origins = ["https://karaoke-me.netlify.app"] # Change once I get an actual production url
  app.config.update(
    CELERY=dict(
      broker_url=os.environ.get("CELERY_BROKER_URL_PROD", "redis://localhost:6379"),
      result_backend=os.environ.get("CELERY_RESULT_BACKEND_PROD", "redis://localhost:6379"),
      task_ignore_result=True,
    )
  )
CORS(app, origins=origins, supports_credentials=True)
oauth = OAuth(app)
oauth.register(
  "auth0",
  client_id=os.environ.get("AUTH0_CLIENT_ID"),
  client_secret=os.environ.get("AUTH0_CLIENT_SECRET"),
  client_kwargs={
    "scope": "openid profile email",
  },
  server_metadata_url=f'https://{os.environ.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

celery = make_celery(app)
celery.conf.update(app.config)

app.register_blueprint(auth.auth_router)
app.register_blueprint(karaoke.karaoke_router)
app.register_blueprint(youtube_dl.youtube_dl_router)

@app.get("/api")
def home():
  return json.dumps({"message": "Hello, World!"})

@app.route("/api/login")
def login():
  return oauth.auth0.authorize_redirect(
    redirect_uri=url_for("callback", _external=True)
  )

@app.route("/api/callback", methods=["GET", "POST"])
def callback():
  print("Callback")
  token = oauth.auth0.authorize_access_token()
  session["user"] = token
  return redirect(app.config["CLIENT_URL"])

@app.route("/api/logout")
def logout():
  session.clear()
  return redirect(
    "https://" + os.environ.get("AUTH0_DOMAIN")
    + "/v2/logout?"
    + urlencode(
      {
        "returnTo": app.config["CLIENT_URL"],
        "client_id": os.environ.get("AUTH0_CLIENT_ID"),
      },
      quote_via=quote_plus,
    )
  )

@app.get("/api/celery-query/<task_id>")
def celery_query(task_id):
  task = make_celery(app).AsyncResult(task_id)
  return json.dumps({"state": task.state, "result": task.result})

if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=5000)