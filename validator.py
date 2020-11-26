from datetime import datetime
import re

def room_validation(arg):
    if arg not in ['l', 'g', 's', 'a']:
        print(f"Invalid room type {arg}. Room type must be l, g, s or a.")
        return False
    return True

def month_validation(arg):
    if arg not in ['january', 'february', 'march', 'april', 'may', 'june',
    'july', 'august', 'september', 'october', 'november', 'december']:
        print(f"Invalid month {arg}.")
        return False
    return True

def date_validation(arg):
    try:
        datetime.strptime(arg, '%d-%m-%Y')
        return True
    except ValueError:
        print("Incorrect date. It should be a valid dd-mm-yyyy")
        return False

def num_arg_validation(valid_num, actual_num):
    if(valid_num != actual_num):
        print (f'Invalid number of arguments. It must be {valid_num}.')
        return False
    return True

def accomodation_validation(arg):
    if arg not in ['sm', 'db']:
        print(f"Invalid accomodation type {arg}. Accomodation type must be sm or db.")
        return False
    return True

def lastname_validation(arg):
    name_format = re.compile('[a-zA-Z]+_[a-zA-Z]+')
    if not name_format.match(arg):
        print(f"Invalid name format {arg}. Name format must be name_lastname (e.g. sira_vegas).")
        return False
    return True

def dni_validation(arg):
    dni_format = re.compile('[0-9]{8}[A-Z]')
    if not dni_format.match(arg):
        print(f"Invalid DNI {arg}. DNI format must be 8 numbers and 1 capital letter (e.g. 12345678K).")
        return False
    return True

def balcony_validation(arg):
    if arg not in ['y', 'n']:
        print(f"Invalid argument#2 {arg}. Argument#2 must be y for balcony or n for no balcony.")
        return False
    return True
    