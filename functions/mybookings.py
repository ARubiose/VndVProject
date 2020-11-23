from functions.utils import print_booking_info

def mybookings(conn, name_lastname, client_ID):
    """Show the bookings by name_lastname and client_ID

        Parameters
        ----------
        conn : Connection to the database
        
        name_lastname: name_lastname value

        client_ID: client_ID value

            
        """
    c = conn.cursor()
    
    # Get booking info
    c.execute(f"SELECT * FROM bookings WHERE CLIENT_ID = '{client_ID}' AND NAME_LASTNAME = '{name_lastname}'")
    bookings = c.fetchall()
    if bookings:   
        for booking in bookings:
            print_booking_info(booking)
        return bookings
    else:
        print ("There is no bookings registered")
