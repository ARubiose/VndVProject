import cmd, sys
from functions import *

class BookItShell(cmd.Cmd):
    intro = 'Welcome to Book it.   Type help to list commands.\n'
    prompt = '(Book it) '
    bookings = {}
    available_rooms = {}

    # ----- commands ----- #
    def do_dummyfunction(self, arg):
        print('Sample function')

    def do_exit(self, arg):
        exit(0)

if __name__ == '__main__':
    #  Check booking file 
    BookItShell().cmdloop()