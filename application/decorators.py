import requests
from flask import Flask, Blueprint, request, jsonify, session
from functools import wraps
from authlib.jose import jwt

# Wrapper for login_required decorator
def login_required(f):
  from flask import current_app as app
  @wraps(f)
  def decorated_function(*args, **kwargs):
    #if "user" not in session:
    #  return jsonify({"error": "Unauthorized"}), 401
    token = request.headers.get("Authorization").split("Bearer ")[1]
    if not token:
      return jsonify({"error": "Unauthorized"}), 401
    jwks = requests.get(f"https://{app.config['AUTH0_DOMAIN']}/.well-known/jwks.json").json()
    try:
      claims = jwt.decode(token, jwks)
      claims.validate()
    except:
      return jsonify({"error": "Unauthorized"}), 401
    return f(*args, **kwargs)
  return decorated_function