from flask import Blueprint, request, jsonify
from schema import Schema, Optional, SchemaError

karaoke_router = Blueprint("karaoke_router", __name__)

karaoke_schema = Schema({
  "user_email": str,
  "karaoke_url": str,
  "karaoke_title": str,
  "type": int,
  Optional("video_url"): str,
  Optional("youtube_url"): str,
}, ignore_extra_keys=False)

@karaoke_router.post("/api/karaoke")
def add_karaoke():
  from application.models.karaokeinfo import KaraokeInfo
  from application import db

  body = request.get_json()
  try:
    karaoke_schema.validate(body)
  except SchemaError as e:
    return jsonify({"message": str(e)}), 400
  
  # Add karaoke to database
  karaoke_info = KaraokeInfo(body)
  try:
    karaoke_info.save_to_db()
  except:
    return jsonify({"message": "An error occurred while saving your karaoke information."}), 500
  return jsonify({"message": "Hello, World!"})