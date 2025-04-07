from app.models import User
from app.utils import EnumUserRole
from app import bcrypt


def check_user_data(
    app,
    email: str,
    username: str,
    password: str,
    user_role: EnumUserRole,
):
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        assert user
        assert user.email == email
        assert user.password != password
        assert bcrypt.check_password_hash(user.password, password)
        assert user.role == user_role