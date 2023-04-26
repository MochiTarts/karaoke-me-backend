import uvicorn, asyncio, os, json, ssl, uuid, shutil, yt_dlp
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from typing import Annotated
from urllib import request, parse
from starlette.background import BackgroundTasks

ssl._create_default_https_context = ssl._create_unverified_context
load_dotenv()

app = FastAPI()
origins = ['*']
app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

abs_cwd = os.path.dirname(os.path.abspath(__file__))


def remove_file(path):
  print(f"Removing {path}")
  shutil.rmtree(path)


@app.get("/youtube-dl")
async def get_youtube(url: str, background_tasks: BackgroundTasks):
  if not url:
    return JSONResponse(status_code=400, content={'message': 'URL is required.'})
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
  background_tasks.add_task(remove_file, f'{abs_cwd}/tmp')
  return FileResponse(path, media_type='audio/mpeg')


if __name__ == "__main__":
  if int(os.environ.get('PROD')) == 1:
    uvicorn.run("app:app", host="0.0.0.0", port=os.environ.get('PORT', 8080), reload=False)
  else:
    print("Running in dev mode...")
    uvicorn.run("app:app", host="0.0.0.0", port=os.environ.get('PORT', 8080), reload=True)