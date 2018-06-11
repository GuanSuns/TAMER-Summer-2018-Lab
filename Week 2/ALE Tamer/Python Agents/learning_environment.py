# learning_environment.py
# Author: Lin Guan
#
# It defines a python learning environment that interacts with python agents
# and displays related information using pygame
# --------------

import sys
import time
import numpy as np
import pygame
import utils
from ale_python_interface import ALEInterface
from python_tamer_agent import BasicTamerAgent, PythonReinforcementAgent


class LearningEnvironment:
    def __init__(self, rom_path=None, agent=None
                 , episodes=10, fps=60, display_width=800, display_height=640, sample_rate=10):
        """
            sample_rate: sample experience every sample_rate (or sample_rate+1) frames
        """
        # if not specified, use the default game rom: pacman
        if rom_path is None:
            rom_path = '/Users/lguan/Documents/Study/Research/Atari-2600-Roms/K-P/ms_pacman.bin'

        # setup agent
        if agent is None:
            raise ValueError('Learning Environment - No specified agent')
        elif not isinstance(agent, PythonReinforcementAgent):
            raise TypeError('The agent should be inherited from PythonReinforcementAgent')
        self.agent = agent

        # setup ALE
        self.ale = ALEInterface()
        self.setup_ale(rom_path)

        # initialize parameters
        self.episodes = episodes
        self.fps = fps
        self.display_width = display_width
        self.display_height = display_height
        self.game_surface_width = 0     # the value will be set after loading the rom
        self.game_surface_height = 0    # the value will be set after loading the rom
        self.sample_rate = sample_rate

        # initialize some useful variables
        self.total_reward = 0
        self.last_sample_frame = 0
        self.sample_from_odd_frame = 1  # by switching between 1 and -1 to sample from even frames and odd frames

    def setup_ale(self, rom_path):
        # use current ale
        ale = self.ale

        # Get & Set the desired settings
        ale.setInt(b'random_seed', 123)

        # Set USE_SDL to true to display the screen. ALE must be compiled
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
        rom_file = str.encode(rom_path)
        print('- Loading ROM - %s' % rom_path)
        ale.loadROM(rom_file)
        print('- Complete loading ROM')

        (game_surface_width, game_surface_height) = ale.getScreenDims()
        print("game surface width/height: "
              + str(game_surface_width) + "/"
              + str(game_surface_height))
        self.game_surface_height = game_surface_height
        self.game_surface_width = game_surface_width

        available_action = ale.getMinimalActionSet()
        print('available action set: ', available_action)

    def start_game(self):
        """
            use this function to start the game
        """
        # get the ALE and agent
        ale = self.ale
        agent = self.agent

        # init pygame
        pygame.init()
        display_screen = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption("Arcade Learning Environment Player Agent Display")

        # init clock
        clock = pygame.time.Clock()
        is_exit = False

        # start episodes
        for episode in range(self.episodes):
            if is_exit:
                break

            self.start_episode()
            state = None

            while not ale.game_over() and not is_exit:
                # get new sample according to the sample_rate
                if self.last_sample_frame + self.sample_rate \
                        >= (ale.getEpisodeFrameNumber() + self.sample_from_odd_frame) \
                        or state is None:
                    np_game_surface = np.zeros(shape=(self.game_surface_height, self.game_surface_width, 3)
                                               , dtype=np.int8)
                    ale.getScreenRGB(np_game_surface)
                    game_rgb = utils.copyBuffer(np_game_surface)
                    # get new state based on current game state
                    state = self.agent.extract_state(game_rgb)

                    # update info
                    self.last_sample_frame = ale.getEpisodeFrameNumber()
                    self.sample_from_odd_frame = -self.sample_from_odd_frame

                # get the action from the agent
                a = agent.getAction(state)
                # apply an action and get the resulting reward
                reward = ale.act(a)
                self.total_reward += reward

                current_time = time.time()
                experience = {'time': current_time, 'reward': reward, 'state': state}
                agent.addExperience(experience)

                # if current agent is Tamer agent, then receive
                if isinstance(agent, BasicTamerAgent):
                    h = self.getHumanSignal()
                    agent.receiveHumanSignal(signal=h)

                # clear screen
                display_screen.fill((0, 0, 0))
                # render game surface
                self.renderGameSurface(ale, display_screen
                                       , self.game_surface_width, self.game_surface_height)
                # display related info
                self.displayRelatedInfo(display_screen, a, self.total_reward)

                pygame.display.flip()

                # process pygame event queue
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        is_exit = True
                        break
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                        is_exit = True
                        break

                # delay (default: 60fps)
                clock.tick(self.fps)

            print('Episode %d ended with score: %d' % (episode, self.total_reward))
            self.end_episode()

        # finalize the game
        self.final()

    def final(self):
        """ This function will be at the every end of this program """
        self.agent.final()

    def start_episode(self):
        """ This function will be at the beginning of each episode """
        self.total_reward = 0
        self.last_sample_frame = self.ale.getEpisodeFrameNumber()
        self.sample_from_odd_frame = 1  # by switching between 1 and -1 to sample from even frames and odd frames
        self.agent.startEpisode()

    def end_episode(self):
        """ This function will be at the end of each episode """
        self.ale.reset_game()
        self.agent.stopEpisode()

    @staticmethod
    def renderGameSurface(ale, screen, game_surface_width, game_surface_height):
        """ render game surface with specified width and height """
        # clear screen
        screen.fill((0, 0, 0))

        # get atari screen pixels and blit them
        numpy_surface = np.zeros(shape=(game_surface_height, game_surface_width, 3), dtype=np.int8)
        ale.getScreenRGB(numpy_surface)
        numpy_surface = np.swapaxes(numpy_surface, 0, 1)

        surf = pygame.pixelcopy.make_surface(numpy_surface)
        screen.blit(pygame.transform.scale2x(surf), (5, 5))

    @staticmethod
    def displayRelatedInfo(screen, action, total_reward):
        """ display related information like reward and action on the screen """
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

    @staticmethod
    def getHumanSignal():
        pressed = pygame.key.get_pressed()
        # positive signal
        if pressed[pygame.K_UP]:
            return 1
        elif pressed[pygame.K_DOWN]:
            return -1
        else:
            return 0


def main():
    agent = BasicTamerAgent()
    agent.initAgent()
    environment = LearningEnvironment(agent=agent)
    environment.start_game()


if __name__ == "__main__":
    main()
