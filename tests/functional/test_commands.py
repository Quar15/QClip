from app.utils import EnumUserRole
from .utils import check_user_data


def test_creating_user(runner, app):
    login = "xyz"
    email = "xyz@xyz.com"
    admin_email = "admin_cmd@admin.com"
    password = "secret123"
    with app.app_context():
        result = runner.invoke(args=[
            'commands', 'create-user',
            '--email', email,
            '--login', login,
            '--password', password,
            '--is-admin', True,
        ])
        assert 'error' not in result.output.lower()
        assert 'Created new user' in result.output
        check_user_data(
            app=app,
            email=email,
            username=login,
            password=password,
            user_role=EnumUserRole.ADMIN
        )

        login = 'testing_admin'
        result = runner.invoke(args=[
            'commands', 'create-user',
            '--email', admin_email,
            '--login', login,
        ])
        assert 'error' not in result.output.lower()
        assert 'Created new user' in result.output
        password = result.output.split('\n')[2]
        check_user_data(
            app=app,
            email=admin_email,
            username=login,
            password=password,
            user_role=EnumUserRole.ADMIN
        )

        result = runner.invoke(args=[
            'commands', 'create-user',
            '--email', admin_email,
            '--login', login,
        ])
        assert 'error' in result.output.lower()


        result = runner.invoke(args=[
            'commands', 'create-user',
        ])
        assert 'usage' in result.output.lower()

        