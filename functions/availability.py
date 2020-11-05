def availability(type, db_connection):
    """ Checks availability in a given type of room 
    :param type: l for luxury, g for gold, s for silver, p for platinum or a for every room
    :param dbConnection: a connection to the DB
    :return: None
    """

    c = db_connection.cursor()
    c.execute(f"SELECT COUNT(*) FROM bookings b INNER JOIN room_types r ON b.ROOM = r.rowid WHERE r.TYPE = {type}")

    count = c.fetchone()[0]

    if count <= 8:
        print('There are ' + str(8 - count) + ' rooms of type ' + type + ' still available')
    else:
        print('No more rooms of ' + type + ' are available')
