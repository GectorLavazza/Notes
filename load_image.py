from os import path

from pygame.image import load

from settings import PATH


def load_image(name):
    fullname = path.join(PATH, name + '.png')

    image = load(fullname)
    image = image.convert_alpha()

    return image
