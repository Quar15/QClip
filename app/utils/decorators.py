from flask import redirect, url_for, flash, session, make_response
from flask_login import current_user
from functools import wraps
from .enums.enum_user_role import EnumUserRole


SESSION_VAR_FLASH_MESSAGE_AVAILABLE = "flash_message_available"
SESSION_VAR_REFRESH_PAGE = "refresh_page"


def admin_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if current_user.role != EnumUserRole.ADMIN:
            flash("Unauthorized", "error")
            return redirect(url_for("main.index"))
        return func(*args, **kwargs)

    return wrap


def add_notification_refresh_header(viewmethod):
    @wraps(viewmethod)
    def new_viewmethod(*args, **kwargs):
        resp = make_response(viewmethod(*args, **kwargs))
        if (SESSION_VAR_FLASH_MESSAGE_AVAILABLE in session and session[SESSION_VAR_FLASH_MESSAGE_AVAILABLE]):
            resp.headers["HX-Trigger"] = "newNotification"
            session[SESSION_VAR_FLASH_MESSAGE_AVAILABLE] = False
        return resp

    return new_viewmethod


def add_page_refresh_header(viewmethod):
    @wraps(viewmethod)
    def new_viewmethod(*args, **kwargs):
        resp = make_response(viewmethod(*args, **kwargs))
        if SESSION_VAR_REFRESH_PAGE in session and session[SESSION_VAR_REFRESH_PAGE]:
            resp.headers["HX-Refresh"] = "true"
            session[SESSION_VAR_REFRESH_PAGE] = False
        return resp

    return new_viewmethod
