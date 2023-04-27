from flask import Flask, Blueprint, request, jsonify, session
from functools import wraps

# Wrapper for login_required decorator
def login_required(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    if "user" not in session:
      return jsonify({"error": "Unauthorized"}), 401
    return f(*args, **kwargs)
  return decorated_function