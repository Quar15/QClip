import pytest
from flask_login import current_user, AnonymousUserMixin
from .conftest import TEST_USER_EMAIL, TEST_USER_PASSWORD
from app.models import User
from app.utils import EnumUserRole


def test_login_user(client, app):
    """Test login system and check if correct session was returned"""
    with client:
        response = client.post(
            "/login",
            data={"email": TEST_USER_EMAIL, "password": TEST_USER_PASSWORD},
        )
        assert current_user.id == 1


def test_failed_login(client, app):
    """Test login route bad data"""
    with client:
        response = client.post(
            "/login",
            data={"email": TEST_USER_EMAIL, "password": f"{TEST_USER_PASSWORD}_WRONG"},
        )

        assert current_user.is_authenticated is False
        assert current_user.is_anonymous is True

    # assert b"Login Unsuccessful" in response.data


@pytest.mark.usefixtures("as_admin")
def test_create_user(client, app):
    """Test creating new user account route by admin"""
    with app.app_context():
        number_of_users_pre_request = User.query.count()

    response = client.post(
        "/admin/user/create",
        data={
            "csrf_token": "TEST",
            "username": "tester2",
            "email": "test2@test.com",
            "password": "testing123",
            "confirm_password": "testing123",
            "user_role": f"{EnumUserRole.USER.name}",
        },
        follow_redirects=True
    )

    assert response.status_code == 200

    with app.app_context():
        assert User.query.count() == (number_of_users_pre_request + 1)
        user = User.query.filter_by(username="tester2").first()
        assert user
        assert user.username == "tester2"
        assert user.email == "test2@test.com"
        assert user.role == EnumUserRole.USER.value

    # Try to create user with same username and data
    response = client.post(
        "/admin/user/create",
        data={
            "csrf_token": "TEST",
            "username": "tester2",
            "email": "test2@test.com",
            "password": "testing123",
            "confirm_password": "testing123",
            "user_role": f"{EnumUserRole.USER.name}",
        },
    )

    assert b"That username is taken" in response.data


@pytest.mark.usefixtures("as_logged_user")
def test_logout(client, app):
    """Test logout route as normal user"""
    client.get("/")
    response = client.get("/logout")
    assert response.status_code == 302
    response = client.get("/", follow_redirects=True)
    assert response.status_code == 200


@pytest.mark.usefixtures("as_logged_user")
def test_login_redirect(client, app):
    """Test login route as logged in user"""
    response = client.get("/login", follow_redirects=False)
    assert response.status_code == 302
    response = client.get("/login", follow_redirects=True)
    assert response.status_code == 200
