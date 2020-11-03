balcony_dict = {"y":1,"n":0}

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

    # Update preference
    if room[2] == selection:
        print("Preference already satisfied")

    else:
        c.execute(f"SELECT QUANTITY FROM room_types WHERE TYPE = '{room[0]}' AND SIZE = '{room[1]}' AND BALCONY = {balcony_dict[room[2]]}")
        available_rooms = c.fetchone()[0]

        c.execute(f"SELECT * FROM bookings WHERE ROOM = '{room[0] + room[1] + selection}' and DATE = '{booking[3]}'")

        if len(c.fetchall()) < available_rooms:
            c.execute(f"UPDATE bookings SET ROOM = '{room[0] + '-' + room[1] + '-' + selection}' where ID = {booking_ID}")
            conn.commit()
            print("Preference saved")
        else:
            print("Room not available")

 

    


    
    

