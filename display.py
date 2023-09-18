import tkinter as tk
from tkinter import ttk

class Display:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Conquer the Galaxy")
        self.root.geometry("1278x226")
        self.left_frame = tk.Frame(master = self.root)
        self.left_frame.grid(row = 0, column = 0)
        self.right_frame = tk.Frame(master = self.root)
        self.right_frame.grid(row = 0, column = 1)

        # Placing buttons:
        self.planet_button = ttk.Button(master = self.left_frame, text = "Planet", command = self.display_planet_data)
        self.buildings_button = ttk.Button(master = self.left_frame, text = "Buildings", command = self.display_building)
        self.research_button = ttk.Button(master = self.left_frame, text = "Research")
        self.drafting_button = ttk.Button(master = self.left_frame, text = "Units")
        self.galaxy_button = ttk.Button(master = self.left_frame, text = "Galaxy", command = self.display_system)
        self.shields_button = ttk.Button(master = self.left_frame, text = "Shields")
        for child in self.left_frame.winfo_children():
            child.pack()

        # Creating planet items
        self.land_display = ttk.Label(master = self.right_frame, text = 0)
        self.land_display_label = ttk.Label(master = self.right_frame, text = "Land:")
        self.gold_display = ttk.Label(master = self.right_frame, text = 0)
        self.gold_display_label = ttk.Label(master = self.right_frame, text = "Gold:")
        self.power_display = ttk.Label(master = self.right_frame, text = 0)
        self.power_display_label = ttk.Label(master = self.right_frame, text = "Power:")
        self.population_display = ttk.Label(master = self.right_frame, text = 0)
        self.population_display_label = ttk.Label(master = self.right_frame, text = "Population:")

        # Creating building items
        self.building_types = ("Houses", "Mines", "Power Plants", "Op Centres", "Psychic Centres", "Barracks")
        self.building_displays = []
        self.building_display_labels = []
        self.building_entries = []
        for i in range(len(self.building_types)):
            self.building_displays.append(ttk.Label(master = self.right_frame, text = 0))
            self.building_display_labels.append(ttk.Label(master = self.right_frame, text = self.building_types[i]))
            self.building_entries.append(ttk.Entry(master = self.right_frame))
        # Need to label columns here!
        # Need to display spare land also
        # Need building numbers to be correct


        """
        self.buildings = {
            "Houses": 80,
            "Mines": 100,
            "Power Plants": 50,
            "Op Centres": 1,
            "Psychic Centres": 1,
            "Barracks": 80
            }
        """


        # Creating research items

        # Creating drafting items

        # Creating shields items

        # Creating system items
        self.tree = ttk.Treeview(master = self.right_frame, columns = ("name", "land", "gold", "pop", "type", "owner"), show = "headings")
        self.tree.heading("name", text = "Name")
        self.tree.heading("land", text = "Land")
        self.tree.heading("gold", text = "Gold")
        self.tree.heading("pop", text = "Population")
        self.tree.heading("type", text = "Type")
        self.tree.heading("owner", text = "Owner")



        #tk.mainloop()

    def display_planet_data(self, player = None):
        for child in self.right_frame.winfo_children():
            child.grid_forget()
        self.land_display.grid(column = 1, row = 0)
        self.land_display_label.grid(column = 0, row = 0)
        self.gold_display.grid(column = 1, row = 1)
        self.gold_display_label.grid(column = 0, row = 1)
        self.power_display.grid(column = 1, row = 2)
        self.power_display_label.grid(column = 0, row = 2)
        self.population_display.grid(column = 1, row = 3)
        self.population_display_label.grid(column = 0, row = 3)
        
    def display_system(self, system = "System 1"):
        for child in self.right_frame.winfo_children():
            child.grid_forget()
        for planet in [planet for planet in self.planets if planet.system == system]:
            self.tree.insert("", tk.END, values = (planet.name, planet.land, planet.gold, planet.pop, planet.type, planet.owner))
        self.tree.grid(row = 0, column = 0, sticky="NSEW")

    def display_building(self):
        for child in self.right_frame.winfo_children():
            child.grid_forget()
        for i in range(len(self.building_types)):
            self.building_displays[i].grid(row = i, column = 1)
            self.building_display_labels[i].grid(row = i, column = 0)



        








# Tabs: Buildings, Research, Drafting, System.
