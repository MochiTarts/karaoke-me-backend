from flask import Flask, Blueprint, request, jsonify, send_file, redirect, url_for

karaoke_router = Blueprint("karaoke_router", __name__)