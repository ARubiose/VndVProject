from functions.utils import print_booking_info

def booking_list(conn, private_key):
    """This command is for the hotel administrator. Shows a list of the bookings in the hotel with the code reservation, 
        date, type of room, accommodation, balcony or not and the name of the client for each booking.

        Parameters
        ----------
        conn : Connection to the database
        
        private_key : Administrator key

        Raises
        ------
        Invalid password
            
        """
    # Check password
    if private_key != 'pass':
        print('Invalid password')
        return

    c = conn.cursor()
    
    # Get bookings info
    c.execute(f"SELECT * FROM bookings")
    bookings = c.fetchall()
    if len(bookings) == 0:   
        print("No bookings.")
    else:
        for booking in bookings:
            print_booking_info(booking)
            