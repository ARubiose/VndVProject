def cancelbooking(conn, name_lastname, client_ID, booking_ID):
    """Cancel a booking by ID, name_lastname, client_ID

        Parameters
        ----------
        conn : Connection to the database
        
        name_lastname: name_lastname value

        client_ID: client_ID value

        booking_ID: booking_ID value

        Raises
        ------
        Booking not found
            
        """
    c = conn.cursor()
    
    # Get booking info
    c.execute(f"SELECT * FROM bookings WHERE ID = '{booking_ID}' AND CLIENT_ID = '{client_ID}' AND NAME_LASTNAME = '{name_lastname}'")
    booking = c.fetchone()
    if booking == None:   
        print("Error. Booking not found")
    else:
        c.execute(f"DELETE FROM bookings where ID = {booking_ID}")
        conn.commit()
        print("Booking cancelled")
