import os
from app.models import User, Video
from app import db, create_app

app = create_app(os.getenv("APP_CONFIG", "app.config.DevelopmentConfig"))
with app.app_context():
    print(f"@INFO: Creating db ({app.config['SQLALCHEMY_DATABASE_URI']})")
    db.create_all()
