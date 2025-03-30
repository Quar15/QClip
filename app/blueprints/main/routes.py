from flask import render_template, Blueprint, url_for, request, redirect, send_file
from app.models import User
from app.utils import admin_required
from flask_login import login_required

main = Blueprint("main", __name__)


@main.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@main.route("/_f/<video_slug>")
def serve_video(video_slug: str):
    return send_file("~/Videos/output.mp4", "video/mp4")

@main.route("/f/<video_slug>")
def serve_video_player(video_slug: str):
    timestamp = request.args.get('t')
    if not timestamp:
        timestamp = 0
    return render_template("serve.html", video_slug="xyz", timestamp=timestamp)
