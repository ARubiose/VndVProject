import unittest
import io
from unittest import mock
from unittest.mock import patch

import app
import database

import sys

from functions.guide import manual
from freezegun import freeze_time

#from constants_test import *

class TestGuide(unittest.TestCase):

    def setUp(self):
        self.cli = app.BookItShell()

    def test_guide(self):
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            self.cli.onecmd('guide')
        actual_result = fake_stdout.getvalue().split()
        expected_result = manual
        self.assertEqual(actual_result, expected_result.split())

class TestDescription(unittest.TestCase):

    def setUp(self):
        self.cli = app.BookItShell()
    
    def test_valid_description(self):
        #Luxury
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            self.cli.onecmd('description l')
        actual_result = fake_stdout.getvalue()
        expected_result = 'Luxury Room: It is the most expensive type of room. We have 8 in total, divided into 2 single rooms (1 of them with a balcony) and 6 double rooms (4 of them with a balcony).\n'
        self.assertEqual(actual_result, expected_result)

        #Gold
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            self.cli.onecmd('description g')
        actual_result = fake_stdout.getvalue()
        expected_result = 'Gold Room: It is the second most expensive type of room. We have 8 in total, divided into 2 single rooms (1 of them with a balcony) and 6 double rooms (3 of them with a balcony).\n'
        self.assertEqual(actual_result, expected_result)

        #Silver
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            self.cli.onecmd('description s')
        actual_result = fake_stdout.getvalue()
        expected_result = 'Silver Room: It is the second cheapest type of room. We have 8 in total, divided into 4 single rooms (2 of them with a balcony) and 4 double rooms (2 of them with a balcony).\n'
        self.assertEqual(actual_result, expected_result)

        #Platinum
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            self.cli.onecmd('description p')
        actual_result = fake_stdout.getvalue()
        expected_result = 'Platinum Room: It is the cheapest type of room. We have 8 in total, divided into 4 single rooms (2 of them with a balcony) and 4 double rooms (2 of them with a balcony).\n'
        self.assertEqual(actual_result, expected_result)


    def test_invalid_description(self):
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            self.cli.onecmd('description j')
        actual_result = fake_stdout.getvalue()
        expected_result = 'Invalid room type j. Room type must be l, g, s or a.\n'
        self.assertEqual(actual_result, expected_result)

    def test_invalid_number_of_arguments_description(self):
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            self.cli.onecmd('description j k')
        actual_result = fake_stdout.getvalue()
        expected_result = 'Invalid number of arguments. It must be 1.\n'
        self.assertEqual(actual_result, expected_result)

class TestAvailability(unittest.TestCase):

    @patch('sys.stdout', new_callable=io.StringIO)
    def setUp(self, outs):
        self.cli = app.BookItShell()
        self.cli.connect('test_database.db')
        database.create_tables(self.cli.conn)

    def tearDown(self):
        database.execute_statement(self.cli.conn, 'DROP TABLE bookings')
        database.execute_statement(self.cli.conn, 'DROP TABLE room_types')

# Delete this one
    def test_availability_future_month_this_year(self):
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            with freeze_time("2020-11-23"):
                self.cli.onecmd('availability December')
        
        actual_result = fake_stdout.getvalue().split('\n')[0]
        expected_result = '01-12-2020'
        self.assertEqual(actual_result, expected_result)

    def test_availability_current_month(self):
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            with freeze_time("2020-11-23"):
                self.cli.onecmd('availability november')
        
        actual_result = fake_stdout.getvalue().split('\n')[0]
        expected_result = '23-11-2020'
        self.assertEqual(actual_result, expected_result)

    def test_availability_month_next_year(self):
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            with freeze_time("2020-11-23"):
                self.cli.onecmd('availability january')
        
        actual_result = fake_stdout.getvalue().split('\n')[0]
        expected_result = '01-01-2021'
        self.assertEqual(actual_result, expected_result)

    def test_availability_with_active_bookings(self):
        database.execute_statement(self.cli.conn, f"INSERT INTO bookings (ROOM, NAME_LASTNAME, BOOKING_DATE, CLIENT_ID) VALUES ('l-sm-n', 'test_name', '30-11-2020', '12345678J')")
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            with freeze_time("2020-11-30"):
                self.cli.onecmd('availability november')
        
        actual_result = fake_stdout.getvalue().split('\n')[1]
        expected_result = "{'l-sm-n': 0, 'l-sm-y': 1, 'l-db-n': 2, 'l-db-y': 4, 'g-sm-n': 1, 'g-sm-y': 1, 'g-db-n': 3, 'g-db-y': 3, 's-sm-n': 2, 's-sm-y': 2, 's-db-n': 2, 's-db-y': 2, 'p-sm-n': 2, 'p-sm-y': 2, 'p-db-n': 2, 'p-db-y': 2}"
        self.assertEqual(actual_result, expected_result)

    def test_availability_with_invalid_month(self):
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            self.cli.onecmd('availability januar')

        actual_result = fake_stdout.getvalue()
        expected_result = 'Invalid month januar.\n'
        self.assertEqual(actual_result, expected_result)

class TestBook(unittest.TestCase):

    @patch('sys.stdout', new_callable=io.StringIO)
    def setUp(self, outs):
        self.cli = app.BookItShell()
        self.cli.connect('test_database.db')
        database.create_tables(self.cli.conn)

    def tearDown(self):
        database.execute_statement(self.cli.conn, 'DROP TABLE bookings')
        database.execute_statement(self.cli.conn, 'DROP TABLE room_types')

    def test_book_with_available_no_balcony_rooms(self):
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            self.cli.onecmd('book 30-11-2020 l sm test_name 12345678J')
        actual_result = fake_stdout.getvalue()
        expected_result = 'Booking confirmed for room type l of size sm without balcony. Booking id: 1\n'
        self.assertEqual(actual_result, expected_result)
    
    def test_book_with_only_balcony_rooms_available(self):
        database.execute_statement(self.cli.conn, f"INSERT INTO bookings (ROOM, NAME_LASTNAME, BOOKING_DATE, CLIENT_ID) VALUES ('l-sm-n', 'test_name', '30-11-2020', '12345678J')")
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            self.cli.onecmd('book 30-11-2020 l sm test_name 12345678J')

        actual_result = fake_stdout.getvalue()
        expected_result = 'Booking confirmed for room type l of size sm with balcony. Booking id: 2\n'
        self.assertEqual(actual_result, expected_result)

    def test_book_with_no_rooms_available(self):
        database.execute_statement(self.cli.conn, f"INSERT INTO bookings (ROOM, NAME_LASTNAME, BOOKING_DATE, CLIENT_ID) VALUES ('l-sm-n', 'test_name', '30-11-2020', '12345678J')")
        database.execute_statement(self.cli.conn, f"INSERT INTO bookings (ROOM, NAME_LASTNAME, BOOKING_DATE, CLIENT_ID) VALUES ('l-sm-y', 'test_name', '30-11-2020', '12345678J')")
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            self.cli.onecmd('book 30-11-2020 l sm test_name 12345678J')

        actual_result = fake_stdout.getvalue()
        expected_result = 'Error. There is no room available\n'
        self.assertEqual(actual_result, expected_result)
    
    def test_book_with_invalid_date(self):
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            self.cli.onecmd('book 29-02-2021 l sm test_name 12345678J')

        actual_result = fake_stdout.getvalue()
        expected_result = 'Incorrect date. It should be a valid dd-mm-yyyy\n'
        self.assertEqual(actual_result, expected_result)
    
    def test_book_with_invalid_room_size(self):
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            self.cli.onecmd('book 30-11-2020 l sb test_name 12345678J')

        actual_result = fake_stdout.getvalue()
        expected_result = 'Invalid accomodation type sb. Accomodation type must be sm or db.\n'
        self.assertEqual(actual_result, expected_result)

    def test_book_with_invalid_name_lastname(self):
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            self.cli.onecmd('book 30-11-2020 l sm _name 12345678J')

        actual_result = fake_stdout.getvalue()
        expected_result = 'Invalid name format _name. Name format must be name_lastname (e.g. sira_vegas).\n'
        self.assertEqual(actual_result, expected_result)

    def test_book_with_invalid_ID(self):
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            self.cli.onecmd('book 30-11-2020 l sm test_name 1234567J')

        actual_result = fake_stdout.getvalue()
        expected_result = 'Invalid DNI 1234567J. DNI format must be 8 numbers and 1 capital letter (e.g. 12345678K).\n'
        self.assertEqual(actual_result, expected_result)

class TestCheck(unittest.TestCase):

    @patch('sys.stdout', new_callable=io.StringIO)
    def setUp(self, outs):
        self.cli = app.BookItShell()
        self.cli.connect('test_database.db')
        database.create_tables(self.cli.conn)
        database.execute_statement(self.cli.conn, f"INSERT INTO bookings (ROOM, NAME_LASTNAME, BOOKING_DATE, CLIENT_ID) VALUES ('l-sm-n', 'test_name', '23-11-2020', '12345678J')")

    def tearDown(self):
        database.execute_statement(self.cli.conn, 'DROP TABLE bookings')
        database.execute_statement(self.cli.conn, 'DROP TABLE room_types')

    def test_check_specific_room(self):
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            check_result = self.cli.onecmd('check 23-11-2020 l')
        actual_result = fake_stdout.getvalue()
        expected_result = ''.join([str({'l-sm-n':0, 'l-sm-y':1, 'l-db-n':2, 'l-db-y':4}), '\n'])
        self.assertEqual(actual_result, expected_result)

    def test_check_all_rooms(self):
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            check_result = self.cli.onecmd('check 23-11-2020 a')
        actual_result = fake_stdout.getvalue()
        expected_result = ''.join([str({'l-sm-n':0, 'l-sm-y':1, 'l-db-n':2, 'l-db-y':4, 'g-sm-n':1, 'g-sm-y':1, 'g-db-n':3, 'g-db-y':3, 
                        's-sm-n':2, 's-sm-y':2, 's-db-n':2, 's-db-y':2, 'p-sm-n':2, 'p-sm-y':2, 'p-db-n':2, 'p-db-y':2}), '\n'])
        self.assertEqual(str(actual_result), expected_result)


class TestPreference(unittest.TestCase):

    @patch('sys.stdout', new_callable=io.StringIO)
    def setUp(self, outs):
        self.cli = app.BookItShell()
        self.cli.connect('test_database.db')
        database.create_tables(self.cli.conn)

    def tearDown(self):
        database.execute_statement(self.cli.conn, 'DROP TABLE bookings')
        database.execute_statement(self.cli.conn, 'DROP TABLE room_types')

    def test_available_preference(self):
        database.execute_statement(self.cli.conn, f"INSERT INTO bookings (ROOM, NAME_LASTNAME, BOOKING_DATE, CLIENT_ID) VALUES ('l-sm-n', 'test_name', '23-11-2020', '12345678J')")
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            self.cli.onecmd('preference 1 y')

        c = self.cli.conn.cursor()
        c.execute("SELECT ROOM FROM bookings WHERE ID = '1'")
        booking = c.fetchone()
        self.assertEqual('y', booking[0].split('-')[2])

        actual_result = fake_stdout.getvalue()
        expected_result = 'Preference saved\n'
        self.assertEqual(actual_result, expected_result)

    def test_preference_already_satisfied(self):
        database.execute_statement(self.cli.conn, f"INSERT INTO bookings (ROOM, NAME_LASTNAME, BOOKING_DATE, CLIENT_ID) VALUES ('l-sm-n', 'test_name', '24-11-2020', '12345678J')")
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            self.cli.onecmd('preference 1 n')
        actual_result = fake_stdout.getvalue()
        expected_result = 'Preference already satisfied\n'
        self.assertEqual(actual_result, expected_result)

    def test_not_available_preference(self):
        database.execute_statement(self.cli.conn, f"INSERT INTO bookings (ROOM, NAME_LASTNAME, BOOKING_DATE, CLIENT_ID) VALUES ('l-sm-y', 'test_name', '24-11-2020', '12345678J')")
        database.execute_statement(self.cli.conn, f"INSERT INTO bookings (ROOM, NAME_LASTNAME, BOOKING_DATE, CLIENT_ID) VALUES ('l-sm-n', 'test_name', '24-11-2020', '12345678J')")
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            self.cli.onecmd('preference 1 n')
        actual_result = fake_stdout.getvalue()
        expected_result = 'Room not available\n'
        self.assertEqual(actual_result, expected_result)

    def test_invalid_balcony_selection(self):
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            self.cli.onecmd('preference 1 k')
        actual_result = fake_stdout.getvalue()
        expected_result = 'Invalid argument#2 k. Argument#2 must be y for balcony or n for no balcony.\n'
        self.assertEqual(actual_result, expected_result)

    def test_invalid_reservation_code(self):
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            self.cli.onecmd('preference 1 n')
        actual_result = fake_stdout.getvalue()
        expected_result = 'Error. Invalid reservation code\n'
        self.assertEqual(actual_result, expected_result)

class TestMybookings(unittest.TestCase):
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def setUp(self, outs):
        self.cli = app.BookItShell()
        self.cli.connect('test_database.db')
        database.create_tables(self.cli.conn)
        database.execute_statement(self.cli.conn, f"INSERT INTO bookings (ROOM, NAME_LASTNAME, BOOKING_DATE, CLIENT_ID) VALUES ('l-sm-y', 'test_name', '23-11-2020', '12345678J')")

    def tearDown(self):
        database.execute_statement(self.cli.conn, 'DROP TABLE bookings')
        database.execute_statement(self.cli.conn, 'DROP TABLE room_types')

    def test_existing_bookings(self):
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            self.cli.onecmd('mybookings test_name 12345678J')
        actual_result = fake_stdout.getvalue()
        expected_result ="""----------------
Booking ID : 1
Name : test
Last name : name
Client ID : 12345678J
Room type : Luxury
Room size : Single bed
Room characteristics : With balcony
Date : 23-11-2020
----------------
"""
        self.assertEqual(actual_result, expected_result)

    def test_unexisting_bookings(self):
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            self.cli.onecmd('mybookings test_invalid 12345678K')
        actual_result = fake_stdout.getvalue()
        expected_result = 'There is no bookings registered\n'
        self.assertEqual(actual_result, expected_result)

class TestCancelmybooking(unittest.TestCase):

    @patch('sys.stdout', new_callable=io.StringIO)
    def setUp(self, outs):
        self.cli = app.BookItShell()
        self.cli.connect('test_database.db')
        database.create_tables(self.cli.conn)
        database.execute_statement(self.cli.conn, f"INSERT INTO bookings (ROOM, NAME_LASTNAME, BOOKING_DATE, CLIENT_ID) VALUES ('l-sm-y', 'test_name', '23-11-2020', '12345678J')")

    def tearDown(self):
        database.execute_statement(self.cli.conn, 'DROP TABLE bookings')
        database.execute_statement(self.cli.conn, 'DROP TABLE room_types')

    def test_cancel_booking_guest(self):
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            self.cli.onecmd('cancelbooking test_name 12345678J 1')
        actual_result = fake_stdout.getvalue()
        expected_result = 'Booking cancelled\n'
        self.assertEqual(actual_result, expected_result)

        c = self.cli.conn.cursor()
        c.execute("SELECT * FROM bookings WHERE ID = '1'")
        booking = c.fetchone()
        self.assertEqual(None, booking)

    def test_cancel_unexisting_booking_guest(self):
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            self.cli.onecmd('cancelbooking test_invalid 12345678J 2')
        actual_result = fake_stdout.getvalue()
        expected_result = 'Error. Booking not found\n'
        self.assertEqual(actual_result, expected_result)

class TestList(unittest.TestCase):
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def setUp(self, outs):
        self.cli = app.BookItShell()
        self.cli.connect('test_database.db')
        database.create_tables(self.cli.conn)

    def tearDown(self):
        database.execute_statement(self.cli.conn, 'DROP TABLE bookings')
        database.execute_statement(self.cli.conn, 'DROP TABLE room_types')

    def test_existing_list(self):
        database.execute_statement(self.cli.conn, f"INSERT INTO bookings (ROOM, NAME_LASTNAME, BOOKING_DATE, CLIENT_ID) VALUES ('l-sm-y', 'test_name', '23-11-2020', '12345678J')")
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            self.cli.onecmd('list pass')
        actual_result = fake_stdout.getvalue()
        expected_result ="""----------------
Booking ID : 1
Name : test
Last name : name
Client ID : 12345678J
Room type : Luxury
Room size : Single bed
Room characteristics : With balcony
Date : 23-11-2020
----------------
"""
        self.assertEqual(actual_result, expected_result)

    def test_unexisting_list(self):
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            self.cli.onecmd('list pass')
        actual_result = fake_stdout.getvalue()
        expected_result = 'No bookings.\n'
        self.assertEqual(actual_result, expected_result)

    def test_invalid_password(self):
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            self.cli.onecmd('list invalidpass')
        actual_result = fake_stdout.getvalue()
        expected_result = 'Invalid password\n'
        self.assertEqual(actual_result, expected_result)
    
class TestCancel(unittest.TestCase):
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def setUp(self, outs):
        self.cli = app.BookItShell()
        self.cli.connect('test_database.db')
        database.create_tables(self.cli.conn)

    def tearDown(self):
        database.execute_statement(self.cli.conn, 'DROP TABLE bookings')
        database.execute_statement(self.cli.conn, 'DROP TABLE room_types')

    def test_cancel_booking_manager(self):
        database.execute_statement(self.cli.conn, f"INSERT INTO bookings (ROOM, NAME_LASTNAME, BOOKING_DATE, CLIENT_ID) VALUES ('l-sm-y', 'test_name', '23-11-2020', '12345678J')")
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            self.cli.onecmd('cancel 1')
        actual_result = fake_stdout.getvalue()
        expected_result ='Booking cancelled\n'
        self.assertEqual(actual_result, expected_result)

        c = self.cli.conn.cursor()
        c.execute("SELECT * FROM bookings WHERE ID = '1'")
        booking = c.fetchone()
        self.assertEqual(None, booking)

    def test_cancel_unexisting_booking_manager(self):
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            self.cli.onecmd('cancel 1')
        actual_result = fake_stdout.getvalue()
        expected_result = 'Error. Booking not found\n'
        self.assertEqual(actual_result, expected_result)

class TestDefaults(unittest.TestCase):
    
    def setUp(self):
        self.cli = app.BookItShell()

    def test_invalid_command(self):
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            self.cli.onecmd('invalid_command')
        actual_result = fake_stdout.getvalue()
        expected_result ='invalid_command is not a valid command\n'
        self.assertEqual(actual_result, expected_result)

if __name__ == '__main__':
    unittest.main()