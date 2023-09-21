import sqlite3

class Database:

    def __init__(self, player_name):
        # Create db or connect:
        self.connection = sqlite3.connect(f"{player_name}.db")
        self.cursor = self.connection.cursor()
        try:
            self.connection.execute('''CREATE TABLE Planets (
                                ID INT NOT NULL,
                                Name TINYTEXT NOT NULL,
                                System TINYTEXT NOT NULL,
                                Land INT,
                                Gold INT,
                                Pop INT,
                                Type TINYTEXT,
                                Owner TINYTEXT,
                                Defence INT,
                                Psy_defence INT,
                                Attack INT);''')
            print("table exists")
        except sqlite3.OperationalError:
            print("Table already exists!")
            self.connection.execute("DELETE FROM Planets;")
        self.connection.commit()

    #def populate_galaxy(self, planet):
    def populate_galaxy(self, values):
        # Adds planet to database
        query = "INSERT INTO Planets(ID, Name, System, Land, Gold, Pop, Type, \
                                Owner, Defence, Psy_defence, Attack) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
        #query_data = (planet.id, planet.name, planet.system, planet.land, planet.gold, planet.pop, planet.type,
        #                        planet.owner, planet.defence, planet.psy_defence, planet.attack)
        query_data = values
        self.connection.execute(query, query_data)
        self.connection.commit()

    def print(self):
        query = "SELECT * FROM Planets"
        self.cursor.execute(query)
        for planet in self.cursor.fetchall():
            print(planet)

    def disconnect(self):
        self.connection.close()

    def load_all_planet_data(self):
        # Retrieves planet data from database, returns as a list of tuples.
        query = "SELECT * FROM Planets"
        self.cursor.execute(query)
        return self.cursor.fetchall()
            
    def load_planet_data(self, name, heading):
        query = f"SELECT {heading} FROM Planets WHERE Name = '{name}'"
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]
    
    def load_system_display(self, system):
        query = f"SELECT Name, Land, Gold, Pop, Type, Owner FROM Planets WHERE System = '{system}'"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
#planet.name, planet.land, planet.gold, planet.pop, planet.type, planet.owner

#sqlite_connection.execute("INSERT INTO Planets(ID, Name, Land, Attack, Defence, Gold, Power) VALUES (1, 'Mars', 500, 0, 500, 10000, 5000);")

#sqlite_connection.commit()

#cursor = sqlite_connection.cursor()

#query = "SELECT * FROM Planets"

#cursor.execute(query)

#print(cursor.fetchall())

#sqlite_connection.close()




"""
sqlite_connection = sqlite3.connect("test.db")

cursor = sqlite_connection.cursor()

query = '''       '''

cursor.execute(query)

cursor.fetchall() --> returns query results as a list

sqlite_connection.commit()

sqlite_connection.close()
"""