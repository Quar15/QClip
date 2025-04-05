import os
import uuid
from flask import (render_template, Blueprint, url_for, session, flash,
                   request, redirect, send_file, current_app)
from flask_login import login_required, current_user
from werkzeug.exceptions import RequestEntityTooLarge
from app import db
from app.models import Video
from app.blueprints.videos.forms import VideoUploadForm
from app.utils import (generate_thumbnail, is_allowed_mime_type, add_page_refresh_header, add_notification_refresh_header,
                       SESSION_VAR_REFRESH_PAGE, SESSION_VAR_FLASH_MESSAGE_AVAILABLE)

videos = Blueprint("videos", __name__)


@videos.route("/_w/<video_slug>")
def serve_video(video_slug: str):
    print("@DEBUG: Trying to show video: " + video_slug)
    video = Video.query.filter_by(slug=video_slug).first()
    if not video:
        return send_file(os.path.join(current_app.root_path, "static/img/not_found.png"))
    return send_file(video.path, "video/mp4")


@videos.route("/_w/<video_slug>/thumbnail")
def serve_video_thumbnail(video_slug: str):
    video = Video.query.filter_by(slug=video_slug).first()
    if not video:
        return send_file(os.path.join(current_app.root_path, "static/img/not_found.png"))
    thumbnail_dir = current_app.config['THUMBNAIL_DIRECTORY']
    thumbnail_path = f"{thumbnail_dir}/{video.slug}.jpg"
    if not os.path.isfile(thumbnail_path):
        return send_file(os.path.join(current_app.root_path, "static/img/not_found.png"))
    return send_file(thumbnail_path, "image/jpg")


@videos.route("/w/<video_slug>")
def serve_video_player(video_slug: str):
    video = Video.query.filter_by(slug=video_slug).first()
    if not video:
        return render_template("serve_fail.html")
    timestamp = request.args.get('t')
    if not timestamp:
        timestamp = 0
    return render_template("serve.html", video=video, timestamp=timestamp)


def validate_file(form: VideoUploadForm) -> (bool, object):
    try:
        file = form.file.data
    except RequestEntityTooLarge:
        flash('File is larger than the limit!', 'error')
        return False, None
    if not file:
        flash('File not provided!', 'error')
        return False, None
    # Naive way of checking
    if '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ['ALLOWED_EXTENSIONS']:
        flash('File is not of allowed type!', 'error')
        return False, None
    # MIME type check
    if not is_allowed_mime_type(file, [f"video/{extension}" for extension in current_app.config['ALLOWED_EXTENSIONS']]):
        flash('File is not of allowed type! (MIME)', 'error')
        return False, None
    return True, file


@videos.route("/partial/upload/form", methods=["GET", "POST"])
@login_required
@add_page_refresh_header
@add_notification_refresh_header
def upload_form():
    form = VideoUploadForm()
    if form.validate_on_submit():
        success, file = validate_file(form)
        if not success:
            session[SESSION_VAR_FLASH_MESSAGE_AVAILABLE] = True
        else:
            # Ensuring required dirs is done on startup
            upload_dir = current_app.config['UPLOAD_DIRECTORY']
            thumbnail_dir = current_app.config['THUMBNAIL_DIRECTORY']

            slug = str(uuid.uuid4())
            file_path = os.path.join(upload_dir, slug)
            file.save(file_path)
            thumbnail_path = os.path.join(thumbnail_dir, f"{slug}.jpg")
            generate_thumbnail(file_path, thumbnail_path)

            video = Video()
            video.pretty_name = form.title.data
            video.slug = slug
            video.path = file_path
            video.user_id = current_user.id
            db.session.add(video)
            db.session.commit()
            flash("Video uploaded successfully", "success")
            session[SESSION_VAR_REFRESH_PAGE] = True

    return render_template(
            'partials/video_upload.html',
            form=form,
            upload_action=url_for('videos.upload_form')
    )
