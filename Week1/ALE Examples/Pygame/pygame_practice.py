import pygame
import os

_image_library = {}


def get_image(path):
        global _image_library
        image = _image_library.get(path)
        if image is None:
                canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
                image = pygame.image.load(canonicalized_path)
                _image_library[path] = image
        return image


def main():
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    done = False
    is_blue = True
    x = 30
    y = 30
    clock = pygame.time.Clock()

    while not done:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                is_blue = not is_blue

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            y -= 3
        if pressed[pygame.K_DOWN]:
            y += 3
        if pressed[pygame.K_LEFT]:
            x -= 3
        if pressed[pygame.K_RIGHT]:
            x += 3

        screen.fill((255, 255, 255))

        screen.blit(get_image('ball.png'), (x, y))

        pygame.display.flip()
        # will block execution until 1/60 seconds have passed
        # since the previous time clock.tick was called.
        clock.tick(60)


if __name__ == "__main__":
    main()
