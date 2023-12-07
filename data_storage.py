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
                                Op_defence INT,
                                Attack INT);''')
            print("table exists")
        except sqlite3.OperationalError:
            print("Table already exists!")
            self.connection.execute("DELETE FROM Planets;")
        self.connection.commit()

    def populate_galaxy(self, values):
        # Adds planet to database
        # Is running many queries slowing things down?
        query = "INSERT INTO Planets(ID, Name, System, Land, Gold, Pop, Type, \
                                Owner, Defence, Psy_defence, Op_defence, Attack) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
        query_data = values
        self.connection.execute(query, query_data)
    
    def tick_planet(self, id, new_gold, new_pop, new_defence, new_attack):
        query = "UPDATE Planets SET Gold = ?, Pop = ?, Defence = ?, Attack = ? WHERE ID = ?"
        query_data = (new_gold, new_pop, new_defence, new_attack, id)
        self.cursor.execute(query, query_data)

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
    
    def update_planet_data(self, name, heading, value):
        query = f"UPDATE Planets SET {heading} = ? WHERE Name = ?"
        query_data = (value, name)
        self.cursor.execute(query, query_data)
    
    def load_system_display(self, system):
        query = f"SELECT Name, Land, Gold, Pop, Type, Owner FROM Planets WHERE System = '{system}'"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def get_planet_names(self, system):
        query = f"SELECT Name FROM Planets WHERE System = '{system}'"
        self.cursor.execute(query)
        return [item[0] for item in self.cursor.fetchall()]
    
    def get_system_list(self):
        query = "SELECT DISTINCT System FROM Planets"
        self.cursor.execute(query)
        return [item[0] for item in self.cursor.fetchall()]
    
    def commit(self):
        self.connection.commit()