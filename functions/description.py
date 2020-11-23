def description(type):
    """ Gives information about rooms 
    :param type: l for luxury, g for gold, s for silver, p for platinum or a for every room
    :return: None
    """
    luxury = 'Luxury Room: It is the most expensive type of room. We have 8 in total, divided into 2 single rooms (1 of them with a balcony) and 6 double rooms (4 of them with a balcony).'
    gold = 'Gold Room: It is the second most expensive type of room. We have 8 in total, divided into 2 single rooms (1 of them with a balcony) and 6 double rooms (3 of them with a balcony).'
    silver = 'Silver Room: It is the second cheapest type of room. We have 8 in total, divided into 4 single rooms (2 of them with a balcony) and 4 double rooms (2 of them with a balcony).'
    platinum = 'Platinum Room: It is the cheapest type of room. We have 8 in total, divided into 4 single rooms (2 of them with a balcony) and 4 double rooms (2 of them with a balcony).'

    print({
        'l':luxury,
        'g': gold,
        's': silver,
        'p': platinum,
        'a': '\n'.join([luxury, gold, silver, platinum])
    }.get(type))
    