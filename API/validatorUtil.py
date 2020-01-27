from .models import User


def validate_email(email):
    if User.objects.filter(email=email).exists():
        return email
    else:
        return None


def validate_username(username):
    if User.objects.filter(email=username).exists():
        return username
    else:
        return None


def validate_password(password, confirm_password):
    if password != confirm_password:
        return None
    else:
        return password


def randomString(string_length=10):
    """Generate a random string of default length"""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))