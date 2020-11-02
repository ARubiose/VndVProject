import cmd, sys, sqlite3
from functions.guide import guide
from functions.description import description
from functions.availability import availability

class BookItShell(cmd.Cmd):
    intro = 'Welcome to Book it.   Type help to list commands.\n'
    prompt = '(Book it) '
    
    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    # ----- commands ----- #
    def do_dummyfunction(self, arg):
        print('Sample function')

    def do_guide(self):
        guide()

    def do_description(self, type):
        description(type)

    def do_availability(self, type):
        availability(type, self.c)

    def do_check(self, arg):
        print('test')

    def do_book(self, arg):
        print('test')

    def do_exit(self, arg):
        exit(0)


def create_table(dbConnection, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    dbConnection.execute(create_table_sql)

def createTables():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    sql_insert_rooms = """ INSERT OR IGNORE INTO room_types(ID, TYPE, SIZE, BALCONY, QUANTITY) VALUES
                        (1, 'l', 'sm', 0, 1),
                        (2, 'l', 'sm', 1, 1),
                        (3, 'l', 'db', 0, 2),
                        (4, 'l', 'db', 1, 4),
                        (5, 'g', 'sm', 0, 1),
                        (6, 'g', 'sm', 1, 1),
                        (7, 'g', 'db', 0, 3),
                        (8, 'g', 'db', 1, 3),
                        (9, 's', 'sm', 0, 2),
                        (10, 's', 'sm', 1, 2),
                        (11, 's', 'db', 0, 2),
                        (12, 's', 'db', 1, 2),
                        (13, 'p', 'sm', 0, 2),
                        (14, 'p', 'sm', 1, 2),
                        (15, 'p', 'db', 0, 2),
                        (16, 'p', 'db', 1, 2) """

    sql_create_room_types_table = """ CREATE TABLE IF NOT EXISTS room_types (
                                    ID integer UNIQUE,
                                    TYPE text NOT NULL,
                                    SIZE text NOT NULL,
                                    BALCONY boolean,
                                    QUANTITY integer,
                                    CONSTRAINT chk_type CHECK (TYPE IN ('l', 'g', 's', 'p', 'a')),
                                    CONSTRAINT chk_size CHECK (SIZE IN ('sm', 'db')),
                                    PRIMARY KEY (TYPE, SIZE, BALCONY)
                                ); """

    sql_create_bookings_table = """ CREATE TABLE IF NOT EXISTS bookings (
                                    ID integer PRIMARY KEY,
                                    TYPE text NOT NULL,
                                    NAME_LASTNAME text NOT NULL,
                                    DATE text NOT NULL,
                                    CLIENT_ID integer NOT NULL,
                                    FOREIGN KEY(TYPE) REFERENCES room_types(ID)
                                ); """

    if c is not None:
        # create projects table
        create_table(c, sql_create_bookings_table)
        create_table(c, sql_create_room_types_table)
        c.execute(sql_insert_rooms)
        conn.commit()

if __name__ == '__main__':
    #  Check booking file 
    createTables()
    BookItShell().cmdloop()