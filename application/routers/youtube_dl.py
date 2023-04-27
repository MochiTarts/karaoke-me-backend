import uuid, os, shutil, yt_dlp, tempfile
from flask import Blueprint, request, jsonify, send_file
from application.decorators import login_required

youtube_dl_router = Blueprint("youtube_dl_router", __name__)

abs_cwd = os.path.dirname(os.path.abspath(__file__)) # ie. /Volumes/SAMSUNG_T5/Documents/karaoke-me-backend/routers

def write_file_to_stream(path):
  temp = tempfile.NamedTemporaryFile()
  with open(path, 'rb') as f:
    shutil.copyfileobj(f, temp)
    temp.flush()
  temp.seek(0)
  shutil.rmtree(f'{abs_cwd}/tmp')
  return temp

@youtube_dl_router.get("/api/youtube-dl")
@login_required
def get_youtube():
  # Get query params
  url = request.args.get('url')
  if not url:
    return jsonify({'message': 'URL is required.'}), 400
  # Use youtube_dl to download the audio file from the given YouTube URL.
  filename = f'{uuid.uuid1().hex}'
  ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': f'{abs_cwd}/tmp/{filename}',
    'nocheckcertificate': True,
    'postprocessors': [{
      'key': 'FFmpegExtractAudio',
      'preferredcodec': 'flac',
      'preferredquality': '192',
    }],
  }
  with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
  
  # Return the audio stream. And remove the file after the request is done.
  path = f'{abs_cwd}/tmp/{filename}.flac'
  tempfile = write_file_to_stream(path)
  return send_file(tempfile, mimetype='audio/mpeg', download_name=f'{filename}.flac')