from calendar import monthrange
from datetime import date, timedelta

from database import get_rooms_quantity

month_dict = {
    'January':1,
    'February':2,
    'March':3,
    'April':4,
    'May':5,
    'June':6,
    'July':7,
    'August':8,
    'September':9,
    'October':10,
    'November':11,
    'December':12
}

def availability(conn, month):
    """ Checks availability in a given type of room 
    :param type: l for luxury, g for gold, s for silver, p for platinum or a for every room
    :param dbConnection: a connection to the DB
    :return: None
    """

    current_date = date.today()
    current_month = current_date.month
    room_quantity = get_rooms_quantity(conn)

    last_day = monthrange(current_date.year, month_dict[month])[1]
    last_day = date(current_date.year, month_dict[month], last_day)
    
    start_day = current_date.day if month_dict[month] == current_month else 1
    start_day = date(current_date.year, month_dict[month], start_day)
    
    c = conn.cursor() 

    # Get all bookings in the time lapse
    c.execute(f"SELECT * FROM bookings WHERE BOOKING_DATE BETWEEN '{start_day.strftime('%d-%m-%Y')}' AND '{last_day.strftime('%d-%m-%Y')}'")
    bookings = c.fetchall()

    # Repeat loop
    aux_date = start_day
    while True:
        aux_dict = room_quantity.copy()
        date_bookings = [booking for booking in bookings if booking[3]==aux_date.strftime('%d-%m-%Y')]
        for date_booking in date_bookings:
            aux_dict[date_booking[1]] -= 1

        print(aux_date)
        print(aux_dict)
        print("*******************")

        # Breaking condition
        if aux_date == last_day:
            break
        aux_date += timedelta(days=1)
        