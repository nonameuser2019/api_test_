import random


def generate_long_name(lenght):
    letters = 'qwertyuiopasdfghjklzxcvbnm'
    name = ''
    for i in range(lenght):
        name += random.choice(letters)
    return name


def get_neccessary_guid(array, pattern):
    for obj in array:
        if pattern in obj['name']:
            return obj
