from database import get_rooms_quantity
from functions.check import check

def preference(conn, booking_ID, selection):
    """Set a preference for whether a room with balcony or without balcony if available.

        Parameters
        ----------
        conn : Connection to the database
        
        reservation_code:

        selection: 'y' if room with balcony preferred or 'n' if room without balcony

        Raises
        ------
        Invalid booking_ID
            
        """
    c = conn.cursor()

    # Get booking info
    c.execute(f'SELECT * FROM bookings WHERE ID = {booking_ID}')
    booking = c.fetchone()
    if booking == None:
        print("Error. Invalid reservation code")
        return

    room = booking[1].split('-')
    preference_room = '-'.join([room[0], room[1], selection])

    # Update preference
    if room[2] == selection:
        print("Preference already satisfied")

    else:
        available_rooms = check(conn, booking[3], room[0])

        if available_rooms[preference_room] > 0:
            c.execute(f"UPDATE bookings SET ROOM = '{preference_room}' where ID = {booking_ID}")
            conn.commit()
            print("Preference saved")
        else:
            print("Room not available")
