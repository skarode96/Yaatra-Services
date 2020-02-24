from daily_commute.models import DailyCommute
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


def validate_journey(journey_id):
    if DailyCommute.objects.filter(id=journey_id).exists():
        return journey_id
    else:
        return None


def validate_user_id(user_id):
    if User.objects.filter(id=user_id).exists():
        return user_id
    else:
        return None
