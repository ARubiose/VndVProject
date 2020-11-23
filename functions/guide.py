manual = """ Book it is a program that permits users to request a reservation of a room in a hotel as well as it permits administrators review all these requests. The available commands are:

description <argument>: It is a helpful text for the client about all the type of rooms or one in specific. 
   - The argument is l for luxury, g for gold, s for silver, p for platinum or a for every room.

availability <argument>: The clients can check the availability of rooms in the hotel for a specific month by running this command.   
   - The argument is the month of his/her interest identified by the name: January, …, December.

check <argument1> <argument2>: The client can check the availability of a room for a specific date. 
   - The argument1 is the date in the form dd-mm-aaaa
   - The argument2 is the type of room to book, being l for luxury, g for gold, s for silver, p for platinum or a for every room.

book <argument1> <argument2> <argument3> <argument4> <argument5>: The client can do the booking by running this command.
   - The argument1 is the date in the same format that above. 
   - The argument2 is the type of room: l,g,s or p (for luxury, gold, silver or platinum).
   - The argument3 is the type of accommodation: sm for simple bed or db for double.
   - The argument4 is the name and last name of the person in the format name_lastname.
   - The argument5 is the ID number without special characters, only numbers are accepted. 

preference <argument1> <argument2>: The client can select if want a room with balcony or not. If the client does not define this, this will assign by default randomly based on available rooms for the selected date.
   - The argument1 is the code of reservation provided in the book command respond.
   - The argument2 is y for room with balcony or n for room without balcony. 

mybookings <argument1> <argument2>: The client can see a list of all his/her bookings.
   - The argument1 is name_lastname.
   - The argument2 s ID number without special characters, only numbers are accepted.

cancelmybooking <argument1> <argument2> <argument3>: The client can cancel any of his/her bookings.

list <argument>: This command is for the hotel administrator. Shows a list of the bookings in the hotel with the code reservation, date, type of room, accommodation, balcony or not and the name of the client for each booking. 
   - The argument is the private key previously provided by the developers only to the administrator.

cancel <argument>: The administrator can to cancel any book based on his own criterion. 
   - The argument is the code reservation that he wants to cancel or the word all for cancelling every reservation.) """

def guide():
    """ Returns functionalities of the Book It program. """

    return manual