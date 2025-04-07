import secrets
import click
from flask import Blueprint
from sqlalchemy.exc import IntegrityError
from app import db, create_app, bcrypt
from app.models import User
from app.utils import EnumUserRole


commands = Blueprint("commands", __name__)


@commands.cli.command("create-user")
@click.option("--email", required=True, help="Used for logging in")
@click.option("--login", default="admin", show_default=True, help="Login is used for display name")
@click.option("--password", default=None, hide_input=True, help="Password for new account")
@click.option("--is-admin", default=True, show_default=True, help="Should new account have admin rights")
def create_user_command(email:str, login: str, password: str, is_admin: bool):
    """Create new user"""
    generated_password = False
    if not password:
        password = secrets.token_urlsafe(10)
        generated_password = True
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    new_user = User(
        email=email,
        username=login,
        password=hashed_password,
        role=(EnumUserRole.ADMIN if is_admin else EnumUserRole.USER)
    )
    try:
        db.session.add(new_user)
        db.session.commit()
        print("@INFO: Created new user")
        print(login)
        if generated_password:
            print(password)
            print("@NOTE: After logging in it is recommended to change the password!")
    except IntegrityError:
        print(f"@ERROR: User {login} already exists")