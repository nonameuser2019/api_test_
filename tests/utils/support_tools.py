import random


def generate_long_name(lenght):
    letters = 'qwertyuiopasdfghjklzxcvbnm'
    name = ''
    for i in range(lenght):
        name += random.choice(letters)
    return name


name = generate_long_name(128)
assert len(name) == 128, 'Wrong names length'
