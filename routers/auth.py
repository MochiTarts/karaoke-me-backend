from flask import Flask, Blueprint, request, jsonify, session
from functools import wraps
from schema import Schema, And, Use, Optional, SchemaError
import re
from decorators import login_required

auth_router = Blueprint("auth_router", __name__)

auth0_user_schema = Schema({
  Optional("app_metadata"): dict,
  Optional("created_at"): str,
  "email": lambda email: re.match(r"^[^@]+@[^@]+\.[^@]+$", email),
  "email_verified": bool,
  Optional("family_name"): str,
  Optional("given_name"): str,
  Optional("identities"): list,
  Optional("locale"): str,
  Optional("last_password_reset"): str,
  Optional("multifactor"): list,
  "name": str,
  "nickname": str,
  Optional("permissions"): list,
  Optional("phone_number"): str,
  Optional("phone_verified"): bool,
  "picture": str,
  "sub": str,
  "updated_at": str,
  Optional("user_id"): str,
  Optional("user_metadata"): dict,
  Optional("username"): str,
}, ignore_extra_keys=False)

@auth_router.get("/api/auth/me")
@login_required
def check_me():
  return jsonify({"Message": "User is authenticated!"}), 200