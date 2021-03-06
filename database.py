ROOMS_TABLE = """ CREATE TABLE IF NOT EXISTS room_types (
                                    TYPE text NOT NULL,
                                    SIZE text NOT NULL,
                                    BALCONY boolean,
                                    QUANTITY integer,
                                    CONSTRAINT chk_type CHECK (TYPE IN ('l', 'g', 's', 'p', 'a')),
                                    CONSTRAINT chk_size CHECK (SIZE IN ('sm', 'db')),
                                    PRIMARY KEY (TYPE, SIZE, BALCONY)
                                ); """

BOOKINGS_TABLE = """ CREATE TABLE IF NOT EXISTS bookings (
                                    ID integer PRIMARY KEY AUTOINCREMENT,
                                    ROOM text NOT NULL,
                                    NAME_LASTNAME text NOT NULL,
                                    BOOKING_DATE text NOT NULL,
                                    CLIENT_ID integer NOT NULL
                                ); """

""" Removed FOREIGN KEY (ROOM) REFERENCES room_types(rowid) """ 

ROOMS = """ INSERT OR IGNORE INTO room_types(TYPE, SIZE, BALCONY, QUANTITY) VALUES
                        ('l', 'sm', 0, 1),
                        ('l', 'sm', 1, 1),
                        ('l', 'db', 0, 2),
                        ('l', 'db', 1, 4),
                        ('g', 'sm', 0, 1),
                        ('g', 'sm', 1, 1),
                        ('g', 'db', 0, 3),
                        ('g', 'db', 1, 3),
                        ('s', 'sm', 0, 2),
                        ('s', 'sm', 1, 2),
                        ('s', 'db', 0, 2),
                        ('s', 'db', 1, 2),
                        ('p', 'sm', 0, 2),
                        ('p', 'sm', 1, 2),
                        ('p', 'db', 0, 2),
                        ('p', 'db', 1, 2) """

balcony_dict = {"y":1,"n":0, "1":"y", "0":"n", '%':'%'}

def execute_statement(connection, statement):
    connection.cursor().execute(statement)
    connection.commit()

def create_tables(conn):
    if conn is not None:
        c = conn.cursor()

        # Create ROOMS table (If does not exist)
        c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='room_types' ''')
        if c.fetchone()[0]==0 : 
            print('Creating table for Rooms...')
            execute_statement(conn, ROOMS_TABLE)
            execute_statement(conn, ROOMS)
        

        # Create bookings table (If does not exist)
        c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='bookings' ''')
        if c.fetchone()[0]==0 : 
            print('Creating table for Bookings...')
            execute_statement(conn, BOOKINGS_TABLE)

# Modifiable dict
def get_rooms_quantity(conn, room_type='%', room_size='%', room_balcony='%'):
        c = conn.cursor()
        c.execute(f"SELECT * FROM room_types WHERE TYPE LIKE '{room_type}' AND SIZE LIKE '{room_size}' AND BALCONY LIKE '{balcony_dict[room_balcony]}'")
        rooms = c.fetchall()
        rooms_available = dict()
        for room_info in rooms:
            key = '-'.join([room_info[0], room_info[1], balcony_dict[str(room_info[2])]])
            rooms_available.update({key:int(room_info[3])})
        return rooms_available
