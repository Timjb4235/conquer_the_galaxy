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
        self.drafting_button = ttk.Button(master = self.left_frame, text = "Units", command = self.display_units)
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
        self.building_values = [0, 0, 0, 0, 0, 0]
        self.building_displays = []
        self.building_display_labels = []
        self.building_entries = []
        for i in range(len(self.building_types)):
            self.building_displays.append(ttk.Label(master = self.right_frame, text = 0))
            self.building_display_labels.append(ttk.Label(master = self.right_frame, text = self.building_types[i]))
            self.building_entries.append(ttk.Entry(master = self.right_frame, width = 2))
        self.current_buildings_title = ttk.Label(master = self.right_frame, text = "Current")
        self.new_buildings_title = ttk.Label(master = self.right_frame, text = "New")
        self.update_button = ttk.Button(master = self.right_frame, text = "Update", command = self.update_building_display)
        self.spare_land_display = ttk.Label(master = self.right_frame, text = 0)
        self.spare_land_display_label = ttk.Label(master = self.right_frame, text = "Spare Land:")


        # Creating research items

        # Creating drafting items
        self.draft_types = ("Soldiers", "Scientists", "Psychics", "Operatives")
        self.draft_values = [0, 0, 0, 0]
        self.draft_displays = []
        self.draft_display_labels = []
        self.draft_entries = []
        for i in range(len(self.draft_types)):
            self.draft_displays.append(ttk.Label(master = self.right_frame, text = 0))
            self.draft_display_labels.append(ttk.Label(master = self.right_frame, text = self.draft_types[i]))
            self.draft_entries.append(ttk.Entry(master = self.right_frame, width = 2))
        self.current_draft_title = ttk.Label(master = self.right_frame, text = "Current")
        self.new_draft_title = ttk.Label(master = self.right_frame, text = "New")
        self.draft_update_button = ttk.Button(master = self.right_frame, text = "Update", command = self.update_draft_display)
        self.draftable_pop_display = ttk.Label(master = self.right_frame, text = 0)
        self.draftable_pop_display_label = ttk.Label(master = self.right_frame, text = "Draftable Population:")

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
        system_data = self.database.load_system_display(system)
        for row in system_data:
            self.tree.insert("", tk.END, values = row)


        #for planet in [planet for planet in self.planets if planet.system == system]:
            #self.tree.insert("", tk.END, values = (planet.name, planet.land, planet.gold, planet.pop, planet.type, planet.owner))

        self.tree.grid(row = 0, column = 0, sticky = "NSEW")

    def display_building(self):
        
        for child in self.right_frame.winfo_children():
            child.grid_forget()
        for i in range(len(self.building_types)):
            self.building_values[i] = self.player.buildings[self.building_types[i]]
            self.building_displays[i].config(text = self.building_values[i])
            self.building_displays[i].grid(row = i + 1, column = 1)
            self.building_display_labels[i].grid(row = i + 1, column = 0)
            self.building_entries[i].grid(row = i + 1, column = 2)            
        self.current_buildings_title.grid(row = 0, column = 1)
        self.new_buildings_title.grid(row = 0, column = 2)
        self.update_button.grid(row = 0, column = 3)
        self.spare_land_display.config(text = self.player.spare_land())
        self.spare_land_display.grid(row = len(self.building_types) + 1, column = 4)
        self.spare_land_display_label.grid(row = len(self.building_types) + 1, column = 3)

    def display_units(self):
        for child in self.right_frame.winfo_children():
            child.grid_forget()
        for i in range(len(self.draft_types)):
            self.draft_values[i] = self.player.units[self.draft_types[i]]
            self.draft_displays[i].config(text = self.draft_values[i])
            self.draft_displays[i].grid(row = i + 1, column = 1)
            self.draft_display_labels[i].grid(row = i + 1, column = 0)
            self.draft_entries[i].grid(row = i + 1, column = 2)   
        self.current_draft_title.grid(row = 0, column = 1)
        self.new_draft_title.grid(row = 0, column = 2)
        self.draft_update_button.grid(row = 0, column = 3)
        self.draftable_pop_display.config(text = self.player.draftable_pop())
        self.draftable_pop_display.grid(row = len(self.building_types) + 1, column = 4)
        self.draftable_pop_display_label.grid(row = len(self.building_types) + 1, column = 3)

    def display_research(self):
        for child in self.right_frame.winfo_children():
            child.grid_forget()


    def get_building_requests(self):
        building_requests = {}
        for i in range(len(self.building_types)):
            try:
                building_requests[self.building_types[i]] = int(self.building_entries[i].get())
            except ValueError:
                building_requests[self.building_types[i]] = 0
        return building_requests
    
    def get_draft_requests(self):
        draft_requests = {}
        for i in range(len(self.draft_types)):
            try:
                draft_requests[self.draft_types[i]] = int(self.draft_entries[i].get())
            except ValueError:
                draft_requests[self.draft_types[i]] = 0
        return draft_requests
    
    def update_building_display(self):
        requests = self.get_building_requests()
        self.player.update_buildings(requests)
        self.display_building()
        for i in range(len(self.building_types)):
            self.building_entries[i].delete(0, "end")

    def update_draft_display(self):
        requests = self.get_draft_requests()
        self.player.draft_units(requests)
        self.display_units()
        for i in range(len(self.draft_types)):
            self.draft_entries[i].delete(0, "end")

# Tabs: Buildings, Research, Drafting, System.