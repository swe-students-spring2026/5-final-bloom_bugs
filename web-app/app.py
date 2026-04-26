# main entry point for the web app
import datetime
import os
import re

import pymongo
from bson.objectid import ObjectId
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for, session
from datetime import timedelta
from flask import Flask, render_template, request
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# create the Flask app
app = Flask(__name__)
# load environment variables from .env file
load_dotenv()
# set the secret key for session management
app.secret_key = os.getenv("SECRET_KEY")
# connect to MongoDB
client = pymongo.MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("MONGO_DB_NAME")]

# set up Spotify API credentials
sp_oauth = SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
    scope="user-read-private user-read-email playlist-modify-public playlist-modify-private",
)

# login route
@app.route("/login")
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

# callback route for Spotify authentication
@app.route("/callback")
def callback():
    code = request.args.get("code")
    token_info = sp_oauth.get_access_token(code)
    access_token = token_info["access_token"]
    sp = spotipy.Spotify(auth=access_token)
    user_info = sp.current_user()
    user_id = user_info["id"]
    # store user info in session
    session["user_id"] = user_id
    session["access_token"] = access_token
    return redirect(url_for("index"))

# logout route
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

