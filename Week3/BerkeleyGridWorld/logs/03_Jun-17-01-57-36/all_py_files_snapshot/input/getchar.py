# getchar.py
#
# A getChar function similar to the getChar function in C
# ------------
import tty
import termios
import sys


def getChar():
    # Returns a single character from standard input
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


if __name__ == '__main__':
    def test():
        while 1:
            ch = getChar()
            if ch.strip() == '':
                print('bye!')
                break
            else:
                print('You pressed %s' % ch)
    test()

