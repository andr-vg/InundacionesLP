from app.models.user import User

def check(user_id, permission):
    return User.has_permission(user_id, permission)

def has_permission(permission, session):
    return permission in session.get("permissions")

