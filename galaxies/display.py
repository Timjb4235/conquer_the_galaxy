import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext as st

class Display:

    def __init__(self, systems, op_missions, database, tick):
        self.root = tk.Tk()
        self.root.title("Conquer the Galaxy")
        self.root.geometry("1378x226")
        self.left_frame = ttk.Frame(master = self.root)
        self.left_frame.grid(row = 0, column = 0, sticky = "nse")
        self.right_frame = ttk.Frame(master = self.root, width = 1178)
        self.right_frame.grid(row = 0, column = 1, sticky = "nsew")
        #self.right_frame.grid_propagate(False)
        self.options_frame = ttk.Frame(master = self.root)
        self.options_frame.grid(row = 0, column = 2, sticky = "ne")
        self.root.columnconfigure(1, weight = 12)
        self.database = database
        self.mode = "system"

        # Placing buttons:
        self.button_frame = ttk.Frame(master = self.left_frame)
        self.button_frame.pack(anchor = "center")
        self.planet_button = ttk.Button(master = self.button_frame, text = "My Planet", command = self.display_planet_data)
        self.buildings_button = ttk.Button(master = self.button_frame, text = "Buildings", command = self.display_building)
        self.research_button = ttk.Button(master = self.button_frame, text = "Research", command = self.display_research)
        self.drafting_button = ttk.Button(master = self.button_frame, text = "Units", command = self.display_units)
        self.galaxy_button = ttk.Button(master = self.button_frame, text = "Galaxy", command = self.display_system)
        self.shields_button = ttk.Button(master = self.button_frame, text = "Shields", command = self.display_shields)
        self.operatives_button = ttk.Button(master = self.button_frame, text = "Operatives", command = self.display_operatives)
        self.military_button = ttk.Button(master = self.button_frame, text = "Military", command = self.display_military)
        for child in self.button_frame.winfo_children():
            child.pack()
        self.save_button = ttk.Button(master = self.options_frame, text = "Save")
        self.load_button = ttk.Button(master = self.options_frame, text = "Load")
        self.info_button = ttk.Button(master = self.options_frame, text = "More Info")
        self.readme_button = ttk.Button(master = self.options_frame, text = "Readme")
        self.tick = tick
        self.end_turn_button = ttk.Button(master = self.options_frame, text = "End Turn", command = self.end_turn)
        self.end_turn_button.pack()

        # Creating planet items
        self.name_display = ttk.Label(master = self.right_frame, text = 0)
        self.name_display_label = ttk.Label(master = self.right_frame, text = "Name:")
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
        self.research_types = ("Space Exploration", "Terraforming", "Lunar Colonies", "Shields", "Fusion Power", "Cloud Cities", "Asteroid Mining", "Stardocks", "Superweapons")
        self.research_values = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        #Should the above be a dict?
        self.sci_displays = []
        self.research_point_displays = []
        self.sci_display_labels = []
        self.sci_entries = []
        for i in range(len(self.research_types)):
            self.sci_displays.append(ttk.Label(master = self.right_frame, text = 0))
            self.sci_display_labels.append(ttk.Label(master = self.right_frame, text = self.research_types[i]))
            self.research_point_displays.append(ttk.Label(master = self.right_frame, text = 0))
            self.sci_entries.append(ttk.Entry(master = self.right_frame, width = 2))
        self.current_scis_title = ttk.Label(master = self.right_frame, text = "Assigned")
        self.new_scis_title = ttk.Label(master = self.right_frame, text = "New")
        self.research_point_title = ttk.Label(master = self.right_frame, text = "Research Points")
        self.update_scis_button = ttk.Button(master = self.right_frame, text = "Update", command = self.update_sci_display)
        self.clear_scis_button = ttk.Button(master = self.right_frame, text = "Reset Scientists", command = self.clear_sci_display)
        self.spare_scis_display = ttk.Label(master = self.right_frame, text = 0)
        self.spare_scis_display_label = ttk.Label(master = self.right_frame, text = "Unassigned Scientists:")

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

        # Creating training items
        self.training_types = ("Attackers", "Defenders", "Elites")
        self.training_values = [0, 0, 0]
        self.training_displays = []
        self.training_display_labels = []
        self.training_entries = []
        for i in range(len(self.training_types)):
            self.training_displays.append(ttk.Label(master = self.right_frame, text = 0))
            self.training_display_labels.append(ttk.Label(master = self.right_frame, text = self.training_types[i]))
            self.training_entries.append(ttk.Entry(master = self.right_frame, width = 2))
        self.current_training_title = ttk.Label(master = self.right_frame, text = "Current")
        self.new_training_title = ttk.Label(master = self.right_frame, text = "New")
        self.training_update_button = ttk.Button(master = self.right_frame, text = "Update", command = self.update_training_display)

        # Creating shields items
        self.shield_types = ("Military Shield:", "Missile Shield:", "Operative Shield:")
        self.shield_percentages = (0, 0, 0)
        self.shield_display_labels = []
        self.shield_cost_displays = []
        self.shield_sliders = []
        for i in range(len(self.shield_types)):
            self.shield_display_labels.append(ttk.Label(master = self.right_frame, text = self.shield_types[i]))
            self.shield_cost_displays.append(ttk.Label(master = self.right_frame, text = 0))
            self.shield_sliders.append(ttk.LabeledScale(master = self.right_frame, from_ = 0, to = 100, width = 300))

        # Creating system items
        self.tree = ttk.Treeview(master = self.right_frame, columns = ("name", "land", "gold", "pop", "type", "owner"), show = "headings")
        self.tree.heading("name", text = "Name")
        self.tree.heading("land", text = "Land")
        self.tree.heading("gold", text = "Gold")
        self.tree.heading("pop", text = "Population")
        self.tree.heading("type", text = "Type")
        self.tree.heading("owner", text = "Owner")
        self.system_var = tk.StringVar()
        self.system_var.set("System One")
        self.system_choice = ttk.OptionMenu(self.options_frame, self.system_var, "System One", *systems, command = self.change_system)

        # Creating targeting menu
        self.target_var = tk.StringVar()
        self.target_var.set(self.database.get_planet_names("System One")[0])
        targets = self.database.get_planet_names("System One")
        self.target_choice = ttk.OptionMenu(self.options_frame, self.target_var, self.target_var.get(), *targets, command = None)

        # Creating operatives items
        self.ops_textbox = st.ScrolledText(master = self.right_frame, width = 147, height = 13.5)
        self.op_mission_var = tk.StringVar()
        self.op_mission_var.set("Select Mission")
        self.op_mission_choice = ttk.OptionMenu(self.options_frame, self.op_mission_var, "Spy", *op_missions)
        self.send_ops_button = ttk.Button(master = self.options_frame, text = "Send Operatives", command = self.send_ops)

        # Creating attack items
        self.attack_textbox = st.ScrolledText(master = self.right_frame, width = 90, height = 13.5)
        self.send_attack_button = ttk.Button(master = self.options_frame, text = "Attack!", command = self.send_attack)
        self.attack_frame = ttk.Frame(master = self.right_frame)
        self.attack_options = ("Generals", "Attackers", "Elites")        
        self.attack_choices = [0, 0, 0]
        self.attack_displays = []
        self.attack_display_labels = []
        self.attack_entries = []
        self.attack_choices_title = ttk.Label(master = self.attack_frame, text = "Maximum")
        self.attack_displays_title = ttk.Label(master = self.attack_frame, text = "Sending")
        self.invasion_popup = tk.Toplevel()
        self.invasion_popup.geometry("400x120")
        self.invasion_popup.protocol("WM_DELETE_WINDOW", self.destroy_planet)
        invasion_message = ttk.Label(master = self.invasion_popup, text = "Attack successful! What would you like to do with the conquered planet?")
        invasion_message.grid(row = 0, rowspan = 3, sticky = "N")
        self.conquer_button = ttk.Button(master = self.invasion_popup, text = "Conquer", command = self.conquer)
        self.vassalise_button = ttk.Button(master = self.invasion_popup, text = "Make Vassal", command = self.make_vassal)
        self.destroy_button = ttk.Button(master = self.invasion_popup, text = "Destroy", command = self.destroy_planet)
        # look up 'tkinter balloon' to get tooltips setup
        self.conquer_button.grid()
        self.vassalise_button.grid()
        self.destroy_button.grid()
        self.invasion_popup.withdraw()        
        for i in range(len(self.attack_options)):
            self.attack_displays.append(ttk.Label(master = self.attack_frame, text = 0))
            self.attack_display_labels.append(ttk.Label(master = self.attack_frame, text = self.attack_options[i]))
            self.attack_entries.append(ttk.Entry(master = self.attack_frame, width = 2))

        # Create generals items
            self.generals_frame = ttk.Frame(master = self.right_frame,  width = 100, height = 13.5)
            self.generals_frame.grid()
            self.generals_tree = ttk.Treeview(master = self.generals_frame, columns = ("general", "attackers", "elites", "turns"), show = "headings")
            self.generals_tree.heading("general", text = "General")
            self.generals_tree.column("general", width = 60)
            self.generals_tree.heading("attackers", text = "Attackers")
            self.generals_tree.column("attackers", width = 60)
            self.generals_tree.heading("elites", text = "Elites")
            self.generals_tree.column("elites", width = 50)
            self.generals_tree.heading("turns", text = "Turns Remaining")
            self.generals_tree.column("turns", width = 100)
            





        # Creating psychic items


        #tk.mainloop()

    def display_planet_data(self):

        self.mode = "planet"
        for child in self.right_frame.winfo_children():
            child.grid_forget()
        self.system_choice.pack_forget()
        self.op_mission_choice.pack_forget()
        self.target_choice.pack_forget()
        self.send_ops_button.pack_forget()
        self.send_attack_button.pack_forget()
        self.name_display.grid(column = 1, row = 0)
        self.name_display_label.grid(column = 0, row = 0)
        self.land_display.grid(column = 1, row = 1)
        self.land_display_label.grid(column = 0, row = 1)
        self.gold_display.grid(column = 1, row = 2)
        self.gold_display_label.grid(column = 0, row = 2)
        self.power_display.grid(column = 1, row = 3)
        self.power_display_label.grid(column = 0, row = 3)
        self.population_display.grid(column = 1, row = 4)
        self.population_display_label.grid(column = 0, row = 4)
        self.name_display.config(text = self.player.name)
        self.land_display.config(text = self.player.land)
        self.gold_display.config(text = self.player.gold)
        self.power_display.config(text = self.player.power)
        self.population_display.config(text = self.player.pop)
        
    def display_system(self):

        self.mode = "system"
        system = self.system_var.get()
        for child in self.right_frame.winfo_children():
            child.grid_forget()
        self.op_mission_choice.pack_forget()
        self.send_ops_button.pack_forget()
        self.send_attack_button.pack_forget()
        system_data = self.database.load_system_display(system)
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in system_data:
            self.tree.insert("", tk.END, values = row)
        self.tree.grid(row = 0, column = 0, sticky = "NSEW")
        self.system_choice.pack()

    def display_building(self):
        
        self.mode = "building"
        for child in self.right_frame.winfo_children():
            child.grid_forget()
        self.system_choice.pack_forget()
        self.op_mission_choice.pack_forget()
        self.send_ops_button.pack_forget()
        self.target_choice.pack_forget()
        self.send_attack_button.pack_forget()
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
        self.mode = "units"
        for child in self.right_frame.winfo_children():
            child.grid_forget()
        self.system_choice.pack_forget()
        self.op_mission_choice.pack_forget()
        self.target_choice.pack_forget()
        self.send_ops_button.pack_forget()
        self.send_attack_button.pack_forget()
        for i in range(len(self.draft_types)):
            self.draft_values[i] = self.player.units[self.draft_types[i]]
            self.draft_displays[i].config(text = self.draft_values[i])
            self.draft_displays[i].grid(row = i + 1, column = 1)
            self.draft_display_labels[i].grid(row = i + 1, column = 0)
            self.draft_entries[i].grid(row = i + 1, column = 2)   
        self.current_draft_title.grid(row = 0, column = 1)
        self.new_draft_title.grid(row = 0, column = 2)
        self.draft_update_button.grid(row = 0, column = 3)
        self.draftable_pop_display.config(text = self.player.draftable_pop)
        self.draftable_pop_display.grid(row = len(self.building_types) + 1, column = 4)
        self.draftable_pop_display_label.grid(row = len(self.building_types) + 1, column = 3)
        for i in range(len(self.training_types)):
            self.training_values[i] = self.player.units[self.training_types[i]]
            self.training_displays[i].config(text = self.training_values[i])
            self.training_displays[i].grid(row = i + 1, column = 6)
            self.training_display_labels[i].grid(row = i + 1, column = 5)
            self.training_entries[i].grid(row = i + 1, column = 7)
        self.current_training_title.grid(row = 0, column = 6)
        self.new_training_title.grid(row = 0, column = 7)
        self.training_update_button.grid(row = 0, column = 8)

    def display_research(self):
        self.mode = "research"
        for child in self.right_frame.winfo_children():
            child.grid_forget()
        self.system_choice.pack_forget()
        self.op_mission_choice.pack_forget()
        self.send_ops_button.pack_forget()
        self.send_attack_button.pack_forget()
        self.target_choice.pack_forget()
        for i in range(len(self.research_types)):
            self.research_values[i] = self.player.research_points[self.research_types[i]]
            self.sci_displays[i].config(text = self.player.assigned_scientists[self.research_types[i]])
            self.sci_displays[i].grid(row = i + 1, column = 1)
            self.sci_display_labels[i].grid(row = i + 1, column = 0)
            self.research_point_displays[i].config(text = self.research_values[i])
            self.research_point_displays[i].grid(row = i + 1, column = 3)
            self.sci_entries[i].grid(row = i + 1, column = 2)
            self.current_scis_title.grid(row = 0, column = 1)
            self.new_scis_title.grid(row = 0, column = 2)
            self.research_point_title.grid(row = 0, column = 3)
            self.update_scis_button.grid(row = 0, column = 4)
            self.clear_scis_button.grid(row = 0, column = 5)
            self.spare_scis_display.config(text = self.player.spare_scientists())
            self.spare_scis_display.grid(row = len(self.building_types) + 1, column = 5)
            self.spare_scis_display_label.grid(row = len(self.building_types) + 1, column = 4)

    def display_shields(self):
        self.mode = "shields"
        for child in self.right_frame.winfo_children():
            child.grid_forget()
        self.system_choice.pack_forget()
        self.op_mission_choice.pack_forget()
        self.send_ops_button.pack_forget()
        self.target_choice.pack_forget()
        self.send_attack_button.pack_forget()
        for i in range(len(self.shield_types)):
            self.shield_display_labels[i].grid(row = i + 1, column = 0)
            self.shield_cost_displays[i].grid(row = i + 1, column = 2)
            self.shield_sliders[i].grid(row = i + 1, column = 1, padx = 10)

    def display_operatives(self, op_mission = "Spy"):
        self.mode = "operatives"
        for child in self.right_frame.winfo_children():
            child.grid_forget()
        self.system_choice.pack()
        self.target_choice.pack()
        self.ops_textbox.grid()
        self.send_ops_button.pack()
        self.ops_textbox.configure(state = "normal")
        self.ops_textbox.delete("1.0", "end")
        self.ops_textbox.insert(tk.END, f"You have {self.player.units['Operatives']} operatives, and {self.player.op_missions} op missions remaining. \nWhat mission would you like to send them on? \n")
        self.ops_textbox.configure(state = "disabled")
        self.op_mission_choice.pack()

    def display_military(self):
        self.mode = "military"
        for child in self.right_frame.winfo_children():
            child.grid_forget()
        self.op_mission_choice.pack_forget()
        self.send_ops_button.pack_forget()
        self.system_choice.pack()
        self.target_choice.pack()
        self.send_attack_button.pack()
        self.attack_frame.grid(row = 0, column = 0)
        self.generals_frame.grid(row = 0, column = 3)
        self.attack_textbox.grid(row = 0, column = 1, sticky = "N")
        self.attack_textbox.configure(state = "normal")
        self.attack_textbox.delete("1.0", "end")
        self.attack_textbox.insert(tk.END, "")
        self.attack_textbox.configure(state = "disabled")
        self.attack_choices_title.grid(row = 0, column = 1, sticky = "N")
        self.attack_displays_title.grid(row = 0, column = 2, sticky = "N")
        for i in range(len(self.attack_options)):
            self.attack_choices[i] = self.player.units[self.attack_options[i]]
            self.attack_displays[i].config(text = self.attack_choices[i])
            self.attack_displays[i].grid(row = i + 1, column = 1)
            self.attack_display_labels[i].grid(row = i + 1, column = 0)
            self.attack_entries[i].grid(row = i + 1, column = 2)
        for row in self.tree.get_children():
            self.tree.delete(row)
        for general in self.player.generals_away:
            data = (1, general.units_taken["Attackers"], general.units_taken["Elites"], general.turns)
            self.generals_tree.insert("", tk.END, values = data)
        self.generals_tree.grid(row = 0, column = 0, sticky = "W")

    def end_turn(self):
        self.tick()
        match self.mode:
            case "planet":
                self.display_planet_data()
            case "system":
                self.display_system()
            case "building":
                self.display_building()
            case "units":
                self.display_units()
            case "research":
                self.display_research()
            case "shields":
                self.display_shields()
            case "operatives":
                self.display_operatives()
            case "military":
                self.display_military()


        



    def change_system(self, system):
        targets = self.database.get_planet_names(system)
        self.target_choice.set_menu(targets[0], *targets)
        self.system_var.set(system)
        if self.mode == "system":
            self.display_system()

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
    
    def get_training_requests(self):
        training_requests = {}
        for i in range(len(self.training_types)):
            try:
                training_requests[self.training_types[i]] = int(self.training_entries[i].get())
            except ValueError:
                training_requests[self.training_types[i]] = 0
        return training_requests
    
    def get_sci_requests(self):
        sci_requests = {}
        for i in range(len(self.research_types)):
            try:
                sci_requests[self.research_types[i]] = int(self.sci_entries[i].get())
            except ValueError:
                sci_requests[self.research_types[i]] = 0
        return sci_requests
    
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

    def update_training_display(self):
        requests = self.get_training_requests()
        self.player.train_units(requests)
        self.display_units()
        for i in range(len(self.training_types)):
            self.training_entries[i].delete(0, "end")

    def update_sci_display(self):
        requests = self.get_sci_requests()
        self.player.update_scis(requests)
        self.display_research()
        for i in range(len(self.research_types)):
            self.sci_entries[i].delete(0, "end")

    def clear_sci_display(self):
        self.player.clear_scis()
        self.display_research()
        
    def send_ops(self):
        # Check op mission number
        mission = self.op_mission_var.get()
        self.ops_textbox.configure(state = "normal")
        if self.player.units["Operatives"] <= 0:
            self.ops_textbox.insert(tk.END, "You do not have enough operatives to carry out this mission! \n")
        elif self.player.op_missions <= 0:
            self.ops_textbox.insert(tk.END, "You do not have any op missions remaining this turn! \n")
        else:
            if mission == "Spy":
                self.ops_textbox.insert(tk.END, self.player.spy(self.target_var.get(), attribute = "Pop", database = self.database))
            elif mission == "Steal":
                self.ops_textbox.insert(tk.END, self.player.steal(self.target_var.get(), database = self.database))
            elif mission == "Kidnap":
                self.ops_textbox.insert(tk.END, self.player.kidnap(self.target_var.get(), database = self.database))
            elif mission == "Sabotage Defences":
                self.ops_textbox.insert(tk.END, self.player.sabotage(self.target_var.get(), database = self.database))
        self.ops_textbox.configure(state = "disabled")

    def send_attack(self):
        # Get information from the display
        attack_values = {}
        for i in range(len(self.attack_options)):
            try:
                attack_values[self.attack_options[i]] = int(self.attack_entries[i].get())
            except ValueError:
                attack_values[self.attack_options[i]] = 0
        # Popup if successful
        if self.player.attack_succeeds(attack_values, self.target_var.get(), database = self.database):
            self.invasion_popup.deiconify()
            self.invasion_popup.grab_set()
        else:
            self.attack_textbox.configure(state = "normal")
            self.attack_textbox.insert(tk.END, self.player.attack_fails())
            self.attack_textbox.configure(state = "disabled")

    def close_popup(self):
        self.invasion_popup.withdraw()
        self.invasion_popup.grab_release()

    def destroy_planet(self):
        target = self.target_var.get()
        # Printing message and gaining resources
        self.attack_textbox.configure(state = "normal")
        self.attack_textbox.insert(tk.END, self.player.destroy_planet(target, self.database))
        self.attack_textbox.configure(state = "disabled")
        # Remove planet from database
        self.database.remove_planet(target)
        # Resetting target menu
        system = self.system_var.get()
        targets = self.database.get_planet_names(system)
        self.target_choice.set_menu(targets[0], *targets)
        # Close window
        self.close_popup()

    def make_vassal(self):
        target = self.target_var.get()
        # Printing message and changing planet status
        self.attack_textbox.configure(state = "normal")
        self.attack_textbox.insert(tk.END, self.player.make_vassal(target, self.database))
        self.attack_textbox.configure(state = "disabled")
        # Resetting target menu
        system = self.system_var.get()
        targets = self.database.get_planet_names(system)
        self.target_choice.set_menu(targets[0], *targets)
        # Close window
        self.close_popup()

    def conquer(self):
        target = self.target_var.get()
        # Printing message and changing planet status
        self.attack_textbox.configure(state = "normal")
        self.attack_textbox.insert(tk.END, self.player.conquer(target, self.database))
        self.attack_textbox.configure(state = "disabled")
        # Resetting target menu
        system = self.system_var.get()
        targets = self.database.get_planet_names(system)
        self.target_choice.set_menu(targets[0], *targets)
        # Close window
        self.close_popup()


    
        





