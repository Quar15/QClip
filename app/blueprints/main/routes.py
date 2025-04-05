from flask import render_template, Blueprint, current_app, request
from flask_login import current_user
from app.models import Video

main = Blueprint("main", __name__)


@main.route("/", methods=["GET"])
def index():
    page = request.args.get('page', 1, type=int)
    videos_page = Video.query.order_by(Video.created_at.desc()).paginate(page=page, per_page=50)
    thumbnail_dir = current_app.config['THUMBNAIL_DIRECTORY']
    return render_template("index.html", videos_page=videos_page, thumbnail_dir=thumbnail_dir, user=current_user)


@main.route("/partials/notifications", methods=["GET"])
def notifications():
    return render_template("partials/notifications.html")
