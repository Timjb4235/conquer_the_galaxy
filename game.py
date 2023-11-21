import data_storage
import display
from random import randint, uniform
import tkinter as tk

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
        self.name = name
        self.land = 500
        self.gold = 10000
        self.power = 5000
        self.pop = 4000
        self.draftable_pop = int(self.pop * 0.01)
        self.op_missions = 10
        self.buildings = {
            "Houses": 80,
            "Mines": 100,
            "Power Plants": 50,
            "Op Centres": 1,
            "Psychic Centres": 1,
            "Barracks": 80
            }
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

        self.units = {
            "Soldiers": 0,
            "Scientists": 0,
            "Psychics": 0,
            "Operatives": 0
        }
        self.shields = {
        }
        self.superweapons = {
        }

    def tick(self):
        # Update player stats
        self.gold += self.pop
        self.gold += 100 * self.buildings["Mines"]
        self.pop = min(self.pop * 1.01, self.buildings["Houses"] * 50)
        # Should this be max?
        self.power = self.power + self.buildings["Power Plants"] * 60 - int(self.pop * 0.1) - sum(self.buildings.values())
        self.power = min(self.power, self.buildings["Power Plants"] * 100)
        # Should this be max?
        if self.op_missions < 10:
            self.op_missions += 1
        for key in self.research_points:
            self.research_points[key] += self.assigned_scientists[key]
        self.update_draftable_pop()
              

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
        try:
            if sum(draft_requests.values()) <= self.draftable_pop and min(draft_requests.values()) >= 0:
                for key in draft_requests:
                    self.units[key] += draft_requests[key]
                    self.draftable_pop -= draft_requests[key]
                    print(self.units["Operatives"])
            else:
                print("Not enough draftable population!")
        except:
            print("Entries must be integers!")

    def spy(self, planet, attribute, database):
        # Called by the display
        self.op_missions -= 1
        planet_op_defence = database.load_planet_data(planet, "Op_defence")
        if self.mission_succeeds(planet_op_defence, type = "spy"):
            # Increases target's op defence, and player takes op losses
            database.update_planet_data(planet, "Op_defence", planet_op_defence + 1)
            op_losses = self.units["Operatives"] // 20
            self.units["Operatives"] -= op_losses       
            return f"Mission successful! You have lost {op_losses} operatives during the mission.\n"
        else:
            # Increases target's op defence, and player takes op losses
            database.update_planet_data(planet, "Op_defence", planet_op_defence + 2)
            op_losses = self.units["Operatives"] // 10
            self.units["Operatives"] -= op_losses
            return f"Mission failed! You have lost {op_losses} operatives during the mission.\n"
        
    def steal(self, planet, attribute, database):
        # Called by the display
        self.op_missions -= 1
        planet_op_defence = database.load_planet_data(planet, "Op_defence")
        if self.mission_succeeds(planet_op_defence, type = "steal"):
            # Increases target's op defence, and player takes op losses
            database.update_planet_data(planet, "Op_defence", planet_op_defence + 2)
            op_losses = self.units["Operatives"] // 20
            self.units["Operatives"] -= op_losses       
            return f"Mission successful! You have lost {op_losses} operatives during the mission.\n"
        else:
            # Increases target's op defence, and player takes op losses
            database.update_planet_data(planet, "Op_defence", planet_op_defence + 3)
            op_losses = self.units["Operatives"] // 10
            self.units["Operatives"] -= op_losses
            return f"Mission failed! You have lost {op_losses} operatives during the mission.\n"


    def mission_succeeds(self, target_op_defence, type):
        modifiers = {
            "spy": 0.7,
            "steal": 1.1,
            "sabotage": 2.0
        }
        pass_threshold = target_op_defence * uniform(0.5, 1.5) * modifiers[type]
        return self.units["Operatives"] >= pass_threshold
        
if __name__ == "__main__":
    game = Game("optesting")
    systems = ["System One", "System Two", "System Three", "System Four", "System Five", "System Six", "System Seven"]
    op_missions = ["Spy", "Steal"]
    sysname_files = [1, 2, 3, 4, 5, 6, 7]
    for system in systems:
        n = sysname_files.pop(randint(0, len(sysname_files) - 1))
        with open(f"names_{n}.txt", "r") as f:
            names = f.readlines()
        for i in range(10):
            game.database.populate_galaxy((10*n + i, names.pop(randint(1, len(names) - 1)), system, 500, 10000, 1000, "Standard Planet", "Independent", 500, 0, 0, 0))
    game.database.commit()
    display = display.Display(systems, op_missions, game.database, game.tick)
    display.player = game.player
    display.display_system()
    tk.mainloop()

