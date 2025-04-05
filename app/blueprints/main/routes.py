from flask import render_template, Blueprint, current_app
from flask_login import login_required
from app.models import Video
import os

main = Blueprint("main", __name__)


@main.route("/", methods=["GET"])
def index():
    videos = Video.query.all()
    thumbnail_dir = os.environ['APP_THUMBNAIL_DIRECTORY']
    return render_template("index.html", videos=videos, thumbnail_dir=thumbnail_dir)
