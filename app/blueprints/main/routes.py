import os
from flask import render_template, Blueprint, url_for, request, redirect, send_file, current_app
from app.models import Video
from app.utils import admin_required
from flask_login import login_required

main = Blueprint("main", __name__)


@main.route("/", methods=["GET"])
def index():
    videos = Video.query.all()
    return render_template("index.html", videos=videos)


@main.route("/_f/<video_slug>")
def serve_video(video_slug: str):
    print("@DEBUG: Trying to show video: " + video_slug)
    video = Video.query.filter_by(slug=video_slug).first()
    if not video:
        return send_file(os.path.join(current_app.root_path, "static/img/not_found.png"))
    return send_file(video.path, "video/mp4")


@main.route("/f/<video_slug>")
def serve_video_player(video_slug: str):
    video = Video.query.filter_by(slug=video_slug).first()
    if not video:
        return render_template("serve_fail.html")
    timestamp = request.args.get('t')
    if not timestamp:
        timestamp = 0
    return render_template("serve.html", video=video, timestamp=timestamp)
