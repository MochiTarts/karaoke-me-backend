from application import db
import datetime

class KaraokeInfo(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  created_at = db.Column(db.DateTime, nullable=False)
  user_email = db.Column(db.String(255), nullable=False)
  karaoke_url = db.Column(db.String(255), nullable=False)
  karaoke_title = db.Column(db.String(255), nullable=False)
  type = db.Column(db.Integer, nullable=False) # 0 = youtube, 1 = video
  video_url = db.Column(db.String(255), nullable=True)
  youtube_url = db.Column(db.String(255), nullable=True)

  def __init__(self, body):
    self.created_at = datetime.datetime.now()
    self.user_email = body["user_email"]
    self.karaoke_url = body["karaoke_url"]
    self.karaoke_title = body["karaoke_title"]
    self.type = body["type"]
    self.video_url = body.get("video_url", None)
    self.youtube_url = body.get("youtube_url", None)

  def save_to_db(self):
    db.session.add(self)
    db.session.commit()