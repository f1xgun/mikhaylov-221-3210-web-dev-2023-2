from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user


def check_rights(need_admin_role: bool = False, need_moderator_role: bool = False):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if need_moderator_role:
                if current_user.is_user():
                    flash('У вас недостаточно прав для выполнения данного действия.', 'warning')
                    return redirect(url_for('index'))

            if need_admin_role:
                if not current_user.is_admin():
                    flash('У вас недостаточно прав для выполнения данного действия.', 'warning')
                    return redirect(url_for('index'))

            return f(*args, **kwargs)

        return decorated_function

    return decorator
