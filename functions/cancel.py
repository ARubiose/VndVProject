def cancel(conn, booking_ID):
    """Delete a booking by ID

        Parameters
        ----------
        conn : Connection to the database

        booking_ID: Booking ID

        Raises
        ------
        Booking not found
            
        """
    c = conn.cursor()
    
    # Get booking info
    c.execute(f"SELECT * FROM bookings WHERE ID = '{booking_ID}'")
    booking = c.fetchone()
    if booking == None:   
        print ("Error. Booking not found")
    else:
        c.execute(f"DELETE FROM bookings where ID = {booking_ID}")
        conn.commit()
        print("Booking cancelled")
        