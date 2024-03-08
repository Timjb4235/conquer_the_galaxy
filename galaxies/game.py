import data_storage
import display
from random import randint, uniform
import tkinter as tk
import json

class Game:

    def __init__(self, name):
        self.name = name
        self.round = 0
        self.phase = 1
        self.database = data_storage.Database(name)
        self.player = Player(name)

    def tick(self):
        # Update player stats:
        self.player.tick()
        # Update stats of other planets:
        planets = self.database.load_all_planet_data()
        for planet in planets:
            new_gold = int(planet[4] * uniform(0.98, 1.03))
            new_pop = int(planet[5] * uniform(0.99, 1.02))
            new_defence = int(planet[8] * uniform(1, 1.1))
            new_attack = int(planet[10] * uniform(1, 1.05))
            self.database.tick_planet(planet[0], new_gold, new_pop, new_defence, new_attack)
        self.database.commit()

class Player:

    def __init__(self, name):
        # Values can be in thousands
        with open("config.json") as f:
            constants = json.load(f)
            starting_resources = constants["player_starting_resources"]
        self.name = name
        self.land = starting_resources["land"]
        self.gold = starting_resources["gold"]
        self.power = starting_resources["power"]
        self.pop = starting_resources["pop"]
        # Make draftable pop a property
        self.draftable_pop = int(self.pop * 0.01)
        self.op_missions = starting_resources["player_stats"]["max_op_missions"]
        self.buildings = starting_resources["buildings"]
        self.research_points = {
            "Space Exploration": 0,
            "Terraforming": 0,
            "Lunar Colonies": 0,
            "Shields": 0,
            "Fusion Power": 0,
            "Cloud Cities": 0,
            "Asteroid Mining": 0,
            "Stardocks": 0,
            "Superweapons": 0
        }
        self.assigned_scientists = {
            "Space Exploration": 0,
            "Terraforming": 0,
            "Lunar Colonies": 0,
            "Shields": 0,
            "Fusion Power": 0,
            "Cloud Cities": 0,
            "Asteroid Mining": 0,
            "Stardocks": 0,
            "Superweapons": 0
        }

        self.units = starting_resources["units"]
        self.shields = {
        }
        self.superweapons = {
        }
        self.generals_away = []

    def tick(self):
        # Update player stats
        self.gold += self.pop
        self.gold += 100 * self.buildings["Mines"]
        self.pop = min(self.pop * 1.01, self.buildings["Houses"] * 50)
        self.power = self.power + self.buildings["Power Plants"] * 60 - int(self.pop * 0.1) - sum(self.buildings.values())
        self.power = max(self.power, self.buildings["Power Plants"] * 100)
        if self.op_missions < 10:
            self.op_missions += 1
        for key in self.research_points:
            self.research_points[key] += self.assigned_scientists[key]
        self.update_draftable_pop()
        # Generals move towards home
        for general in self.generals_away:
            general.turns -= 1
            print(general)
            if general.turns <= 0:
                # General returns
                self.units["Generals"] += 1
                for key in general.units_taken:
                    self.units[key] += general.units_taken[key]
                self.generals_away.remove(general)
              

    def spare_land(self):
        return self.land - sum(self.buildings.values())
    
    def spare_scientists(self):
        return self.units["Scientists"] - sum(self.assigned_scientists.values())
    
    def update_draftable_pop(self):
        # Returns the number of draftable pop for the turn
        self.draftable_pop = int(self.pop * 0.01)
        
    def update_buildings(self, build_requests):
        try:
            if sum(build_requests.values()) <= self.spare_land() and min(build_requests.values()) >= 0:
                for key in self.buildings:
                    self.buildings[key] += build_requests[key]
            else:
                print("Not enough spare land!")
        except:
            print("Entries must be integers!")

    def update_scis(self, sci_requests):
        try:
            if sum(sci_requests.values()) <= self.spare_scientists() and min(sci_requests.values()) >= 0:
                for key in self.assigned_scientists:
                    self.assigned_scientists[key] += sci_requests[key]
            else:
                print("Not enough spare scientists!")
        except:
            print("Entries must be integers!")

    def clear_scis(self):
        for key in self.assigned_scientists:
            self.assigned_scientists[key] = 0

    def draft_units(self, draft_requests):
        # Called by the display. Display should only pass in valid input.
        if sum(draft_requests.values()) > self.draftable_pop:
            raise ValueError("Not enough draftable pop!")
        elif min(draft_requests.values()) < 0:
            raise ValueError("Entries must be integers")
        for key in draft_requests:
            self.units[key] += draft_requests[key]
            self.draftable_pop -= draft_requests[key]

    def train_units(self, training_requests):
        # Called by the display. Display should only pass in valid input.
        if sum(training_requests.values()) > self.units["Soldiers"]:
            raise ValueError("Not enough soldiers!")
        elif min(training_requests.values()) < 0:
            raise ValueError("Entries must be integers!")
        for key in training_requests:
                    self.units[key] += training_requests[key]
                    self.units["Soldiers"] -= training_requests[key]


    def spy(self, planet, attribute, database):
        # Called by the display. Check for magic numbers.
        self.op_missions -= 1
        planet_op_defence = database.load_planet_data(planet, "Op_defence")
        if self.mission_succeeds(planet_op_defence, type = "Spy"):
            # Increases target's op defence, and player takes op losses
            database.update_planet_data(planet, "Op_defence", planet_op_defence + 1)
            op_losses = self.units["Operatives"] // 20
            self.units["Operatives"] -= op_losses       
            return (f"Mission successful! You have lost {op_losses} operatives during the mission.\n" +
            # Provides data
            f"{planet.strip()} has {database.load_planet_data(planet, attribute)} {attribute}. \n" +
            f"You have {self.units['Operatives']} operatives, and {self.op_missions} op missions remaining. \n" +
            "What mission would you like to send them on? \n")
        else:
            # Increases target's op defence, and player takes op losses
            database.update_planet_data(planet, "Op_defence", planet_op_defence + 2)
            op_losses = self.units["Operatives"] // 10
            self.units["Operatives"] -= op_losses
            return (f"Mission failed! You have lost {op_losses} operatives during the mission.\n" +
            f"You have {self.units['Operatives']} operatives, and {self.op_missions} op missions remaining. \n" +
            "What mission would you like to send them on? \n")
        
    def steal(self, planet, database):
        #temp. Put in game constants instead. Check for magic numbers.
        gold_per_op = 2
        # Called by the display
        self.op_missions -= 1
        planet_op_defence = database.load_planet_data(planet, "Op_defence")
        if self.mission_succeeds(planet_op_defence, type = "Steal"):
            # Increases target's op defence, and player takes op losses
            database.update_planet_data(planet, "Op_defence", planet_op_defence + 2)
            op_losses = self.units["Operatives"] // 20
            self.units["Operatives"] -= op_losses
            # Steal gold
            planet_gold_amount = database.load_planet_data(planet, "Gold")
            theft_size = min(self.units["Operatives"] * gold_per_op, planet_gold_amount)
            self.gold += theft_size
            database.update_planet_data(planet, "Gold", planet_gold_amount - theft_size)
            return (f"Mission successful! You have lost {op_losses} operatives during the mission.\n" +
            f"You have stolen {theft_size} Gold from {planet.strip()}.\n" + 
            f"You have {self.units['Operatives']} operatives, and {self.op_missions} op missions remaining. \n" +
            "What mission would you like to send them on? \n")
        else:
            # Increases target's op defence, and player takes op losses
            database.update_planet_data(planet, "Op_defence", planet_op_defence + 3)
            op_losses = self.units["Operatives"] // 10
            self.units["Operatives"] -= op_losses
            return (f"Mission failed! You have lost {op_losses} operatives during the mission.\n" + 
            f"You have {self.units['Operatives']} operatives, and {self.op_missions} op missions remaining. \n" +
            "What mission would you like to send them on? \n")
        
    def kidnap(self, planet, database):
        #temp. Put in game constants instead. Check for magic numbers.
        pop_per_op = 1
        # Called by the display
        self.op_missions -= 1
        planet_op_defence = database.load_planet_data(planet, "Op_defence")
        if self.mission_succeeds(planet_op_defence, type = "Kidnap"):
            # Increases target's op defence, and player takes op losses
            database.update_planet_data(planet, "Op_defence", planet_op_defence + 2)
            op_losses = self.units["Operatives"] // 20
            self.units["Operatives"] -= op_losses
            # Steal pop
            planet_pop_amount = database.load_planet_data(planet, "Pop")
            theft_size = min(self.units["Operatives"] * pop_per_op, planet_pop_amount)
            self.pop += theft_size
            database.update_planet_data(planet, "Pop", planet_pop_amount - theft_size)
            return (f"Mission successful! You have lost {op_losses} operatives during the mission.\n" +
            f"You have stolen {theft_size} Population from {planet.strip()}.\n" + 
            f"You have {self.units['Operatives']} operatives, and {self.op_missions} op missions remaining. \n" +
            "What mission would you like to send them on? \n")
        else:
            # Increases target's op defence, and player takes op losses
            database.update_planet_data(planet, "Op_defence", planet_op_defence + 3)
            op_losses = self.units["Operatives"] // 10
            self.units["Operatives"] -= op_losses
            return (f"Mission failed! You have lost {op_losses} operatives during the mission.\n" + 
            f"You have {self.units['Operatives']} operatives, and {self.op_missions} op missions remaining. \n" +
            "What mission would you like to send them on? \n")
        
    def sabotage(self, planet, database):
        defence_per_op = 0.5
        # Called by the display. Check for magic numbers.
        self.op_missions -= 1
        planet_op_defence = database.load_planet_data(planet, "Op_defence")
        if self.mission_succeeds(planet_op_defence, type = "Sabotage Defences"):
            # Decreases target's op defence, and player takes op losses
            database.update_planet_data(planet, "Op_defence", planet_op_defence - 3)
            op_losses = self.units["Operatives"] // 10
            self.units["Operatives"] -= op_losses
            # Sabotage defence
            planet_defence = database.load_planet_data(planet, "Defence")
            defence_reduction = min(self.units["Operatives"] * defence_per_op, planet_defence)
            database.update_planet_data(planet, "Defence", planet_defence - defence_reduction)
            return (f"Mission successful! You have lost {op_losses} operatives during the mission.\n" +
            f"You have successfully reduced the defences of {planet.strip()}.\n" + 
            f"You have {self.units['Operatives']} operatives, and {self.op_missions} op missions remaining. \n" +
            "What mission would you like to send them on? \n")
        else:
            # Increases target's op defence, and player takes op losses
            database.update_planet_data(planet, "Op_defence", planet_op_defence + 4)
            op_losses = self.units["Operatives"] // 10
            self.units["Operatives"] -= op_losses
            return (f"Mission failed! You have lost {op_losses} operatives during the mission.\n" + 
            f"You have {self.units['Operatives']} operatives, and {self.op_missions} op missions remaining. \n" +
            "What mission would you like to send them on? \n")

    def mission_succeeds(self, target_op_defence, type):
        modifiers = {
            "Spy": 0.7,
            "Steal": 1.1,
            "Kidnap": 1.2,
            "Sabotage Defences": 2.0
        }
        pass_threshold = target_op_defence * uniform(0.5, 1.5) * modifiers[type]
        return self.units["Operatives"] >= pass_threshold

    def attack_succeeds(self, units_sent, target, database):
        # Adjust for magic numbers, for scaling with more units, for readability
        for key in units_sent:
            if self.units[key] < units_sent[key]:
                raise ValueError(f"Not enough {key} to send!")
        target_defence = database.load_planet_data(target, "Defence")
        target_land = database.load_planet_data(target, "Land")
        attack = units_sent["Attackers"] * 4 + units_sent["Elites"] * 8
        # Set up units out with generals
        army_divisions = units_sent["Generals"]
        unit_division = {
            "Attackers": units_sent["Attackers"] // army_divisions,
            "Elites": units_sent["Elites"] // army_divisions
        }
        for i in range(army_divisions):
            self.generals_away.append(GeneralAway(unit_division, (12 * (i + 1)) // army_divisions))
            self.units["Generals"] -= 1
        self.units["Attackers"] -= units_sent["Attackers"]
        self.units["Elites"] -= units_sent["Elites"]
        # Set up unit losses
        return attack > max(target_defence, target_land)
    
    def destroy_planet(self, planet, database):
        destruct_retrieval = 0.005
        salvage = (database.load_planet_data(planet, "Gold"), database.load_planet_data(planet, "Pop"), database.load_planet_data(planet, "Land"))
        gold_retrieved = int(destruct_retrieval * salvage[0])
        pop_retrieved = int(destruct_retrieval * salvage[1])
        land_retrieved = int(destruct_retrieval * salvage[2])
        self.gold += gold_retrieved
        self.pop += pop_retrieved
        self.land += land_retrieved
        return (f"{planet.strip()} has been destroyed! We have recovered {gold_retrieved} Gold, {pop_retrieved} Population and {land_retrieved} Land from the debris.")
    
    def make_vassal(self, planet, database):
        database.update_planet_data(planet, "Owner", self.name)
        database.update_planet_data(planet, "Type", "Vassal")
        return (f"{planet.strip()} has been made a vassal state of our empire.")
    
    def conquer(self, planet, database):
        database.update_planet_data(planet, "Owner", self.name)
        database.update_planet_data(planet, "Type", "Conquered")
        return (f"We have occupied {planet.strip()}.")

    def attack_fails(self):
        # Set up units out with generals
        # Unit losses
        # Add detail to message
        return "Attack unsuccessful!"

class GeneralAway:

    def __init__(self, units_taken, turns):
        self.units_taken = units_taken
        self.turns = turns

    def __repr__(self):
        return f"Attackers: {self.units_taken['Attackers']} + Elites: {self.units_taken['Elites']} + Turns left: {self.turns}"
  
    def __del__(self):
        pass
        
if __name__ == "__main__":
    game = Game("optesting2")
    systems = ["System One", "System Two", "System Three", "System Four", "System Five", "System Six", "System Seven"]
    op_missions = ["Spy", "Steal", "Kidnap", "Sabotage Defences"]
    sysname_files = [1, 2, 3, 4, 5, 6, 7]
    for system in systems:
        n = sysname_files.pop(randint(0, len(sysname_files) - 1))
        with open(f"names_{n}.txt", "r") as f:
            names = f.readlines()
        for i in range(10):
            game.database.populate_galaxy((10*n + i, names.pop(randint(1, len(names) - 1)), system, 500, 10000, 1000, "Standard Planet", "Independent", 0, 0, 1, 0))
    game.database.commit()
    display = display.Display(systems, op_missions, game.database, game.tick)
    display.player = game.player
    display.display_system()
    tk.mainloop()

