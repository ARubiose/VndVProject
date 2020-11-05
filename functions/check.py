from database import get_rooms_quantity

def check(conn, booking_date, room_type):
    """Check the availability of a room for a specific date.

        Parameters
        ----------
        conn : Connection to the database
        
        Booking_date: Date

        room_type: Type of room (l,g,s,p)
            
        """

    c = conn.cursor()
    
    # Get booking info
    if room_type == 'a':
        c.execute(f"SELECT * FROM bookings WHERE BOOKING_DATE = '{booking_date}'")
    else:
        c.execute(f"SELECT * FROM bookings WHERE BOOKING_DATE = '{booking_date}' AND ROOM LIKE '{room_type}-%'")

    bookings = c.fetchall()

    available_rooms = get_rooms_quantity(conn) if room_type == 'a' else get_rooms_quantity(conn, room_type=room_type)

    for booking in bookings:
        available_rooms[booking[1]] -= 1

    return available_rooms
