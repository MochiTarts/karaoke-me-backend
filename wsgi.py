from application import init_app
from flask import session, redirect, url_for, jsonify
from urllib.parse import quote_plus, urlencode
from application.tasks import make_celery

app, oauth, celery = init_app()

@app.get("/api")
def home():
  return jsonify({"message": "Hello, World!"}), 200

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
    "https://" + app.config["AUTH0_DOMAIN"]
    + "/v2/logout?"
    + urlencode(
      {
        "returnTo": app.config["CLIENT_URL"],
        "client_id": app.config["AUTH0_CLIENT_ID"],
      },
      quote_via=quote_plus,
    )
  )

@app.get("/api/celery-query/<task_id>")
def celery_query(task_id):
  task = make_celery(app).AsyncResult(task_id)
  return jsonify({"state": task.state, "result": task.result}), 200

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)