import cmd
import sys 

# Functions #
from functions.guide import guide
from functions.description import description
from functions.availability import availability
from functions.check import check
from functions.book import book
from functions.preference import preference
from functions.mybookings import mybookings
from functions.cancelbooking import cancelbooking
from functions.booking_list import booking_list
from functions.cancel import cancel
from validator import *

# Database #
import sqlite3
from database import create_tables

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
        print (guide())

    def do_description(self, arg):
        args = arg.split()
        if(num_arg_validation(1, len(args)) and room_validation(arg)):
            description(arg)

    def do_availability(self, month):
        month_lower = month.lower()
        args = month.split()
        if(num_arg_validation(1, len(args)) and month_validation(month_lower)):
            availability(self.conn, month_lower)

    def do_check(self, arg):
        args = arg.split()
        if (num_arg_validation(2, len(args)) and date_validation(args[0]) and room_validation(args[1])) :
            print(check(self.conn, args[0], args[1]))

    def do_book(self, arg):
        args = arg.split()
        if (num_arg_validation(5, len(args)) and date_validation(args[0]) and room_validation(args[1]) and 
        accomodation_validation(args[2]) and lastname_validation(args[3]) and dni_validation(args[4])):
            book(self.conn, args[0], args[1], args[2], args[3], args[4])

    def do_preference(self, arg):
        args = arg.split()
        if (num_arg_validation(2, len(args)) and balcony_validation(args[1])) :
            preference(self.conn, args[0], args[1])

    def do_mybookings(self, arg):
        args = arg.split()
        if (num_arg_validation(2, len(args)) and lastname_validation(args[0]) and dni_validation(args[1])):
            mybookings(self.conn, args[0], args[1])

    def do_cancelbooking(self, arg):
        args = arg.split()
        if (num_arg_validation(3, len(args)) and lastname_validation(args[0]) and dni_validation(args[1])):
            cancelbooking(self.conn, args[0], args[1], args[2])
    
    def do_list(self, private_key):
        args = private_key.split()
        if (num_arg_validation(1, len(args))):
            booking_list(self.conn, private_key)
    
    def do_cancel(self, booking_ID):
        args = booking_ID.split()
        if (num_arg_validation(1, len(args))):
            cancel(self.conn, booking_ID)

    def do_exit(self, arg):
        exit(0)

    # ----- override commands ----- #

    def default(self, arg):
        ''' Print a command not recognized error message '''
        print(f"{arg} is not a valid command")

if __name__ == '__main__':
    # Console object
    console = BookItShell()

    # Setup. Database
    console.connect('bookings.db')
    create_tables(console.conn)

    # Console loop
    console.cmdloop()
    