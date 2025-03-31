import os
import uuid
from flask import (render_template, Blueprint, url_for,
                   request, redirect, send_file, current_app)
from flask_login import login_required
from werkzeug.exceptions import RequestEntityTooLarge
from app import db
from app.models import Video
from app.utils import is_allowed_mime_type

videos = Blueprint("videos", __name__)


@videos.route("/_f/<video_slug>")
def serve_video(video_slug: str):
    print("@DEBUG: Trying to show video: " + video_slug)
    video = Video.query.filter_by(slug=video_slug).first()
    if not video:
        return send_file(os.path.join(current_app.root_path, "static/img/not_found.png"))
    return send_file(video.path, "video/mp4")


@videos.route("/f/<video_slug>")
def serve_video_player(video_slug: str):
    video = Video.query.filter_by(slug=video_slug).first()
    if not video:
        return render_template("serve_fail.html")
    timestamp = request.args.get('t')
    if not timestamp:
        timestamp = 0
    return render_template("serve.html", video=video, timestamp=timestamp)


@videos.route("/upload", methods=["POST"])
@login_required
def upload():
    try:
        file = request.files['file']
    except RequestEntityTooLarge:
        return 'File is larger than the limit!'
    if not file:
        return redirect(url_for('main.index'))

    # Naive way of checking
    if '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ['ALLOWED_EXTENSIONS']:
        return 'File is not a video!'  # @TODO: Create pretty error
    # MIME type check
    if not is_allowed_mime_type(file, [f"video/{extension}" for extension in current_app.config['ALLOWED_EXTENSIONS']]):
        return 'File is not a video! (MIME)'  # @TODO: Create pretty error

    slug = str(uuid.uuid4())
    file_path = os.path.join(current_app.config['UPLOAD_DIRECTORY'], slug)
    file.save(file_path)
    video = Video()
    video.pretty_name = "XYZ"  # @TODO
    video.slug = slug
    video.path = file_path
    video.user_id = 1  # @TODO
    db.session.add(video)
    db.session.commit()

    return redirect(url_for('main.index'))
