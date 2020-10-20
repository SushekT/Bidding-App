import string
import random


def generatetoken():
    token = ''
    combination = string.ascii_letters+ string.digits
    for i in range(15):
        token = token + str(random.choice(combination))
    return token