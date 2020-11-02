def availability(type, dbConnection):
    """ Checks availability in a given type of room 
    :param type: l for luxury, g for gold, s for silver, p for platinum or a for every room
    :param dbConnection: a connection to the DB
    :return: None
    """
    select_availability = "SELECT COUNT(*) FROM room_types WHERE TYPE = ?"
    dbConnection.execute(select_availability, (type))
    rows = dbConnection.fetchall()
    for row in rows:
        print(row)
    count = dbConnection.fetchone()[0]
    print(count)
    if count <= 8:
        print('There are ' + str(8 - count) + ' rooms of type ' + type + ' still available')
    else:
        print('No more rooms of ' + type + ' are available')
