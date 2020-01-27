import random
import string


def randomString(string_length=10):
    """Generate a random string of default length"""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))