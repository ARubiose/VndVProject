import cmd
import sys 

# Functions #
from functions.guide import guide
from functions.description import description
from functions.availability import availability
from functions.preference import preference
from functions.mybookings import mybookings
from functions.cancelbooking import cancelbooking
from functions.booking_list import booking_list
from functions.cancel import cancel

# Database #
from database import create_tables
import sqlite3

class BookItShell(cmd.Cmd):
    intro = 'Welcome to Book it.   Type guide to list commands.\n'
    prompt = '(Book it) '
    conn = None

    # Connection to the database #
    def connect(self, database_file):
        try:
            self.conn = sqlite3.connect(database_file)
            print("Opened database successfully")
        except:
            print('Error connecting to database...')

    # ----- commands ----- #
    def do_guide(self, arg):
        guide()

    def do_description(self, type):
        description(type)

    def do_availability(self, type):
        availability(type, self.c)

    def do_check(self, arg):
        print('test')

    def do_book(self, arg):
        print('test')

    def do_preference(self, arg):
        args = arg.split()
        if (len(args) != 2) :
            print('Invalid number of arguments')
            return
        preference(self.conn, args[0], args[1])

    def do_mybookings(self, arg):
        args = arg.split()
        if (len(args) != 2) :
            print('Invalid number of arguments')
            return
        mybookings(self.conn, args[0], args[1])

    def do_cancelbooking(self, arg):
        args = arg.split()
        if (len(args) != 3) :
            print('Invalid number of arguments')
            return
        cancelbooking(self.conn, args[0], args[1], args[2])
    
    def do_list(self, private_key):
        booking_list(self.conn, private_key)
    
    def do_cancel(self, booking_ID):
        cancel(self.conn, booking_ID)

    def do_exit(self, arg):
        exit(0)

    # ----- override commands ----- #
    def do_help(self, arg):
        guide()

    def default(self, arg):
        ''' Print a command not recognized error message '''
        print(f" {arg} is not a valid command")

if __name__ == '__main__':
    # Console object
    console = BookItShell()

    # Setup. Database
    console.connect('bookings.db')
    create_tables(console.conn)

    # Console loop
    console.cmdloop()
    