from user.models import User


def validate_email(email):
    if User.objects.filter(email=email).exists():
        return email
    else:
        return None


def validate_username(username):
    if User.objects.filter(username=username).exists():
        return username
    else:
        return None


def validate_password(password, confirm_password):
    if password != confirm_password:
        return None
    else:
        return password
