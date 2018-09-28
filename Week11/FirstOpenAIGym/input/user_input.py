# user_input.py
#
# The module that uses multi-thread to get user inputa asynchronously
# ------------

import threading
from input.getchar import getChar


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

        # handle the case when no inputa received
        if len(self.inputs) == 0:
            value = None
        else:
            value = self.inputs[-1]
            if is_clear:
                self.inputs = list()

        self.lock.release()
        return value


class ReceiveInputThread(threading.Thread):
    """ receive user inputa from keyboard asynchronously """
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


class UserInputModule:
    def __init__(self, is_asyn=True):
        """ is_aysn: control whether to receive user inputa asynchronously """
        self.is_asyn = is_asyn
        self.is_terminated = False

        if is_asyn:
            self.inputs = ThreadSafeInputList()
            self.input_thread = ReceiveInputThread(self.inputs)
            self.input_thread.start()

    def getInput(self):
        if self.is_asyn:
            return self.inputs.get_last(is_clear=True)
        else:
            if self.is_terminated:
                return None

            ch = getChar()
            if ch is not None and ch.strip() == 'q':
                self.is_terminated = True
                return None
            return ch

    def isTerminated(self):
        if self.is_asyn:
            return self.input_thread.shutdown_flag
        else:
            return False


if __name__ == '__main__':
    pass


