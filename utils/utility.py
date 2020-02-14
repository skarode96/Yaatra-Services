import random
import string
from user import models

def randomString(string_length=10):
    """Generate a random string of default length"""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))


def update_user_rating(username, update_rating):
    """ Average Rating """
    user = models.User.objects.get(username=username)
    total_rating_count = user.total_rating_count
    old_rating = user.rating
    new_rating = old_rating * (total_rating_count/(total_rating_count+1)) + update_rating/(total_rating_count+1)
    user.rating = new_rating
    total_rating_count += 1
    user.total_rating_count = total_rating_count
    user.save()
    return new_rating