import pytest
from app import create_app, db, bcrypt
from app.models import User
from app.utils import EnumUserRole


TEST_USER_USERNAME = "tester"
TEST_USER_EMAIL = "test@test.com"
TEST_USER_PASSWORD = "testing123"
TEST_USER_ROLE = EnumUserRole.USER

TEST_ADMIN_USERNAME = "admin"
TEST_ADMIN_EMAIL = "admin@admin.com"
TEST_ADMIN_PASSWORD = "admin123"
TEST_ADMIN_ROLE = EnumUserRole.ADMIN


@pytest.fixture()
def app():
    app = create_app("app.config.TestingConfig")

    with app.app_context():
        db.create_all()

    test_user = User(
        username=TEST_USER_USERNAME,
        email=TEST_USER_EMAIL,
        password=bcrypt.generate_password_hash(TEST_USER_PASSWORD).decode("utf-8"),
        role=TEST_USER_ROLE.value,
    )

    test_admin_user = User(
        username=TEST_ADMIN_USERNAME,
        email=TEST_ADMIN_EMAIL,
        password=bcrypt.generate_password_hash(TEST_ADMIN_PASSWORD).decode("utf-8"),
        role=TEST_ADMIN_ROLE.value,
    )

    with app.app_context():
        db.session.add(test_user)
        db.session.add(test_admin_user)
        db.session.commit()

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture()
def as_logged_user(client, app):
    """Log in as test user"""
    return client.post(
        "/login",
        data={"email": TEST_USER_EMAIL, "password": TEST_USER_PASSWORD},
        follow_redirects=True,
    )


@pytest.fixture()
def as_admin(client, app):
    """Log in as test user"""
    return client.post(
        "/login",
        data={"email": TEST_ADMIN_EMAIL, "password": TEST_ADMIN_PASSWORD},
        follow_redirects=True,
    )
