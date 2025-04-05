from flask import render_template, Blueprint, current_app
from app.models import Video

main = Blueprint("main", __name__)


@main.route("/", methods=["GET"])
def index():
    videos = Video.query.all()
    thumbnail_dir = current_app.config['THUMBNAIL_DIRECTORY']
    return render_template("index.html", videos=videos, thumbnail_dir=thumbnail_dir)
