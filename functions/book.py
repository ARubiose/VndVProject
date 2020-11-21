from database import get_rooms_quantity
from functions.check import check 

def book(conn, booking_date, room_type, accommodation_type, name_lastname, client_ID):
    """Book a room

        Parameters
        ----------
        conn : Connection to the database

        Raises
        ------
        Booking not available
            
        """
    c = conn.cursor()
    
    # Get booking availability
    available_rooms = check(conn, booking_date, room_type)
    available_room = False

    # Balcony selection
    if available_rooms['-'.join([room_type, accommodation_type, 'n'])] > 0:
        available_room = True
        c.execute(f"INSERT INTO bookings (ROOM, NAME_LASTNAME, BOOKING_DATE, CLIENT_ID) VALUES ('{'-'.join([room_type, accommodation_type, 'n'])}', '{name_lastname}', '{booking_date}', '{client_ID}')")
    elif available_rooms['-'.join([room_type, accommodation_type, 'y'])] > 0:
        available_room = True
        c.execute(f"INSERT INTO bookings (ROOM, NAME_LASTNAME, BOOKING_DATE, CLIENT_ID) VALUES ('{'-'.join([room_type, accommodation_type, 'y'])}', '{name_lastname}', '{booking_date}', '{client_ID}')")

    # Booking registrastion
    if available_room:
        print(f'Booking confirmed. Booking id: {c.lastrowid}')
        conn.commit()
    else:
        print("Error. There is no room available")
