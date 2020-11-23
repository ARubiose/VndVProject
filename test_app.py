import unittest
import io
from unittest import mock
from unittest.mock import patch

import app
import database

import sys

from functions.guide import manual

#TODO
class TestGuide(unittest.TestCase):

    def setUp(self):
        self.cli = app.BookItShell()

    def test_guide(self):
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            self.cli.onecmd('guide')
        actual_result = fake_stdout.getvalue().split()
        expected_result = manual
        self.assertEqual(actual_result, expected_result.split())

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
        print(booking)
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


if __name__ == '__main__':
    unittest.main()