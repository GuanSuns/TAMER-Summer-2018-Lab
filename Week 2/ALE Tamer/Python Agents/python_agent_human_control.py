# python_agent_human_control.py
# Author: Lin Guan
#
# This modified ale_python_test_pygame.py by Ben Goodrich to provide a fully interactive experience allowing the player
# to play.
# keys are:
# arrow keys -> up/down/left/right
# SPACE -> fire button

import sys
import numpy as np
from ale_python_interface import ALEInterface
import pygame

import scipy
import scipy.misc

from action_table import key_action_table


def main():
    if len(sys.argv) < 2:
        dir_rom = '/Users/lguan/Documents/Study/Research/Atari-2600-Roms/K-P/ms_pacman.bin'
    else:
        dir_rom = sys.argv[1]

    ale = ALEInterface()

    # Get & Set the desired settings
    ale.setInt(b'random_seed', 123)

    # Set USE_SDL to true to display the screen. ALE must be compilied
    # with SDL enabled for this to work. On OSX, pygame init is used to
    # proxy-call SDL_main.
    USE_SDL = False
    if USE_SDL:
        # mac OS
        if sys.platform == 'darwin':
            pygame.init()
            ale.setBool('sound', False)  # Sound doesn't work on OSX
        elif sys.platform.startswith('linux'):
            ale.setBool('sound', True)

        ale.setBool('display_screen', True)

    # Load the ROM file
    rom_file = str.encode(dir_rom)
    print('- Loading ROM - %s' % dir_rom)
    ale.loadROM(rom_file)
    print('- Complete loading ROM')

    (game_surface_width, game_surface_height) = ale.getScreenDims()
    print("game surface width/height: "
          + str(game_surface_width) + "/"
          + str(game_surface_height))

    (display_width, display_height) = (800, 640)
    print 'display width/height', (display_width, display_height)

    available_action = ale.getLegalActionSet()
    print available_action

    # init pygame
    pygame.init()
    display_screen = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption("Arcade Learning Environment Player Agent Display")

    # init clock
    clock = pygame.time.Clock()
    is_exit = False

    # Play 10 episodes
    for episode in range(10):
        if is_exit:
            break

        total_reward = 0

        while not ale.game_over() and not is_exit:

            a = getActionFromKeyboard()
            # Apply an action and get the resulting reward
            reward = ale.act(a)
            total_reward += reward
            # clear screen
            display_screen.fill((0, 0, 0))
            # render game surface
            renderGameSurface(ale, display_screen, (game_surface_width, game_surface_height))
            # display related info
            displayRelatedInfo(display_screen, a, total_reward)

            pygame.display.flip()

            # process pygame event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_exit = True
                    break
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    is_exit = True
                    break

            # delay to 60fps
            clock.tick(60.)

        print('Episode %d ended with score: %d' % (episode, total_reward))
        ale.reset_game()


def rgb2gray(rgb):
    return np.dot(rgb[..., :3], [0.299, 0.587, 0.114])


def copyBuffer(source):
    dest = np.ndarray(shape=(172, 160))
    for row in range(172):
        for col in range(160):
            dest[row, col] = source[row, col]
    return dest


def renderGameSurface(ale, screen, game_surface_dim):
    # clear screen
    screen.fill((0, 0, 0))

    # get atari screen pixels and blit them
    numpy_surface = np.zeros(shape=(game_surface_dim[1], game_surface_dim[0], 3), dtype=np.int8)
    ale.getScreenRGB(numpy_surface)

    gray = rgb2gray(numpy_surface.copy()).astype(int)
    copy_gray = copyBuffer(gray)
    frame_id = ale.getFrameNumber()
    scipy.misc.imsave('/Users/lguan/Desktop/Others/Pacman/frame_%d.png' % frame_id, copy_gray)

    numpy_surface = np.swapaxes(numpy_surface, 0, 1)
    surf = pygame.pixelcopy.make_surface(numpy_surface)
    screen.blit(pygame.transform.scale2x(surf), (5, 5))


def displayRelatedInfo(screen, action, total_reward):
    line_pos = 20
    # display current action
    font = pygame.font.SysFont("Ubuntu Mono", 32)
    text = font.render("Current Action: " + str(action), 1, (208, 208, 255))
    height = font.get_height() * 1.2
    screen.blit(text, (380, line_pos))
    line_pos += height

    # display reward
    font = pygame.font.SysFont("Ubuntu Mono", 30)
    text = font.render("Total Reward: " + str(total_reward), 1, (208, 255, 255))
    screen.blit(text, (380, line_pos))


def getActionFromKeyboard():
    # get the keys
    keys = 0
    pressed = pygame.key.get_pressed()
    keys |= pressed[pygame.K_UP]
    keys |= pressed[pygame.K_DOWN] << 1
    keys |= pressed[pygame.K_LEFT] << 2
    keys |= pressed[pygame.K_RIGHT] << 3
    keys |= pressed[pygame.K_SPACE] << 4

    action = key_action_table[keys]
    return action


if __name__ == "__main__":
    main()
