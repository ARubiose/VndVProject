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
    print(f"""----------------
Booking ID : {booking[0]}
Name : {full_name[0]}
Last name : {full_name[1]}
Client ID : {booking[4]}
Room type : {room_type[room[0]]}
Room size : {room_size[room[1]]}
Room characteristics : {room_balcony[room[2]]}
Date : {booking[3]}
----------------"""    
    )