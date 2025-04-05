from flask import render_template, Blueprint, current_app, flash
from flask_login import current_user
from app.models import Video

main = Blueprint("main", __name__)


@main.route("/", methods=["GET"])
def index():
    videos = Video.query.all()
    thumbnail_dir = current_app.config['THUMBNAIL_DIRECTORY']
    return render_template("index.html", videos=videos, thumbnail_dir=thumbnail_dir, user=current_user)


@main.route("/partials/notifications", methods=["GET"])
def notifications():
    return render_template("partials/notifications.html")
