import sys
from random import randrange
from ale_python_interface import ALEInterface
import pygame

key_action_table = (
    0,  # 00000 none
    2,  # 00001 up
    5,  # 00010 down
    2,  # 00011 up/down (invalid)
    4,  # 00100 left
    7,  # 00101 up/left
    9,  # 00110 down/left
    7,  # 00111 up/down/left (invalid)
    3,  # 01000 right
    6,  # 01001 up/right
    8,  # 01010 down/right
    6,  # 01011 up/down/right (invalid)
    3,  # 01100 left/right (invalid)
    6,  # 01101 left/right/up (invalid)
    8,  # 01110 left/right/down (invalid)
    6,  # 01111 up/down/left/right (invalid)
    1,  # 10000 fire
    10,  # 10001 fire up
    13,  # 10010 fire down
    10,  # 10011 fire up/down (invalid)
    12,  # 10100 fire left
    15,  # 10101 fire up/left
    17,  # 10110 fire down/left
    15,  # 10111 fire up/down/left (invalid)
    11,  # 11000 fire right
    14,  # 11001 fire up/right
    16,  # 11010 fire down/right
    14,  # 11011 fire up/down/right (invalid)
    11,  # 11100 fire left/right (invalid)
    14,  # 11101 fire left/right/up (invalid)
    16,  # 11110 fire left/right/down (invalid)
    14   # 11111 fire up/down/left/right (invalid)
)


def main():
    if len(sys.argv) < 2:
        dir_rom = '/Users/lguan/Documents/Study/Research/Atari-2600-Roms/T-Z/Tennis.bin'
    else:
        dir_rom = sys.argv[1]

    ale = ALEInterface()

    # Get & Set the desired settings
    ale.setInt(b'random_seed', 123)

    # Set USE_SDL to true to display the screen. ALE must be compilied
    # with SDL enabled for this to work. On OSX, pygame init is used to
    # proxy-call SDL_main.
    USE_SDL = True
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

    # Play 10 episodes
    for episode in range(10):
        total_reward = 0
        while not ale.game_over():
            a = getActionFromKeyboard()
            # Apply an action and get the resulting reward
            reward = ale.act(a)
            total_reward += reward
        print('Episode %d ended with score: %d' % (episode, total_reward))
        ale.reset_game()


def getActionFromKeyboard():
    action = 0
    return action


if __name__ == "__main__":
    main()
