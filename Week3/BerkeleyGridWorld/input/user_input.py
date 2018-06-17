# user_input.py
#
# The module that uses multi-thread to get user input asynchronously
# ------------

import threading
from getchar import getChar
import pygame


class ThreadSafeInputList:
    def __init__(self):
        self.lock = threading.Lock()
        self.inputs = list()

    def push(self, value, is_clear=False):
        self.lock.acquire()

        if is_clear:
            self.inputs = list()
        self.inputs.append(value)

        self.lock.release()

    def get_last(self, is_clear=False):
        self.lock.acquire()

        # handle the case when no input received
        if len(self.inputs) == 0:
            value = None
        else:
            value = self.inputs[-1]
            if is_clear:
                self.inputs = list()

        self.lock.release()
        return value


class ReceiveInputThread(threading.Thread):
    """ receive user input from keyboard asynchronously """
    def __init__(self, thread_safe_list, is_clear=False):
        threading.Thread.__init__(self)
        self.thread_safe_list = thread_safe_list
        self.is_clear = is_clear

        # The shutdown_flag is a boolean value that
        # indicates whether the thread should be terminated.
        self.shutdown_flag = False

    def run(self):
        while not self.shutdown_flag:
            ch = getChar()
            # kill itself when it receive ' ' (space)
            if ch is not None and ch.strip() == '':
                self.shutdown_flag = True
            self.thread_safe_list.push(ch, self.is_clear)


class PygameUserInputModule():
    def __init__(self):
        self.shutdown_flag = False

        # init pygame
        pygame.init()
        pygame.display.set_caption('User Input')
        self.screen = pygame.display.set_mode((250, 120))

    def getInput(self):
        ch = None
        # Event filtering
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.shutdown_flag = True
                elif event.key == pygame.K_UP:
                    ch = 'A'
                elif event.key == pygame.K_DOWN:
                    ch = 'B'
                elif event.key == pygame.K_a:
                    ch = 'a'
                elif event.key == pygame.K_b:
                    ch = 'b'

        self.screen.fill((0, 0, 0))
        pygame.display.flip()
        return ch

    def isTerminated(self):
        return self.shutdown_flag


class UserInputModule():
    def __init__(self):
        self.inputs = ThreadSafeInputList()
        self.input_thread = ReceiveInputThread(self.inputs)
        self.input_thread.start()

    def getInput(self):
        return self.inputs.get_last(is_clear=True)

    def isTerminated(self):
        return self.input_thread.shutdown_flag


if __name__ == '__main__':
    def main():
        user_input_module = PygameUserInputModule()
        while not user_input_module.isTerminated():
            input_value = user_input_module.getInput()
            if input_value is not None:
                print('-- get user input ' + str(input_value))

    main()

