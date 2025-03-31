from flask import render_template, Blueprint
from flask_login import login_required
from app.models import Video

main = Blueprint("main", __name__)


@main.route("/", methods=["GET"])
def index():
    videos = Video.query.all()
    return render_template("index.html", videos=videos)
