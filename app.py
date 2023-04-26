import os
import json
from flask import Flask
from flask_cors import CORS


app = Flask(__name__)
origins = []
if int(app.config["DEBUG"]):
  origins = ["http://localhost:3000"]
else:
  origins = ["https://karaoke-me.netlify.app"] # Change once I get an actual production url
CORS(app, origins=origins)


@app.get("/api")
def hello_world():
  return json.dumps({"message": "Hello, World!"})


if __name__ == "__main__":
  os.environ["FLASK_DEBUG"] = "1"
  app.run(debug=True, host="0.0.0.0", port=5000)