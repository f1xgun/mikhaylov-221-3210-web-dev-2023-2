from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user


def check_rights(required_role, check_same_user=False):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = kwargs.get('user_id', None)

            if not current_user.has_role(required_role):
                if not (check_same_user and user_id and current_user.is_authenticated and current_user.id == str(user_id)):
                    flash('У вас недостаточно прав для доступа к данной странице.', 'warning')
                    return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
