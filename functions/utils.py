room_type = {
    'l':'Luxury',
    'g': 'Gold',
    's': 'Silver',
    'p': 'Platinum'
}

room_size = {
    'sm':'Single bed',
    'db':'Dobule bed'
}

room_balcony = {
    'n':'Without balcony',
    'y':'With balcony'
}

def print_booking_info(booking):
    room = booking[1].split('-')
    full_name = booking[2].split('_')
    print(f"""
    ----------------\n
    Booking ID : {booking[0]}\n
    Name : {full_name[0]}\n
    Last name : {full_name[1]}\n
    Client ID : {booking[4]}\n
    Room type : {room_type[room[0]]}\n
    Room size : {room_size[room[1]]}\n
    Room characteristics : {room_balcony[room[2]]}\n
    Date : {booking[3]}\n
    ----------------\n
    """    
    )