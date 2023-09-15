"""
First ideas: 

-Enemy planets are simple. Type, defence, psy defence, shields, money, pop, sometimes attack, ownership.

-Can destroy, conquer (make vassal), mind control, steal/kidnap, hit with weapons

-Stats change on each tick

-home planet has money, power, pop, ops, troops, shields, weapons, psychics, research...

-psychics are a way of peacefully conquering, equivalent to cultural invasion in civ 4





"""
#import tkinter as tk

# root = tk.Tk()

# buildings_button = tk.Button()
# research_button = tk.Button()
# training_button = tk.Button()
# shields_button = tk.Button()



class Game():
    
    def __init__(self):
        self.round = 0
        self.phase = 1
        self.player = Player()

class Planet():
#-Enemy planets are simple. Type, defence, psy defence, shields, money, pop, sometimes attack, ownership.
    def __init__(self, name, system, land, gold, pop, type, owner, defence, psy_defence, attack):
        self.name = name
        self.system = system
        self.land = land
        self.gold = gold
        self.pop = pop
        self.type = type
        self.owner = owner
        self.defence = defence
        self.psy_defence = psy_defence
        self.attack = attack


class Player():

    def __init__(self):
        # Values can be in thousands
        self.land = 500
        self.gold = 10000
        self.power = 5000
        self.pop = 5000
        self.buildings = {
            "Houses": 80,
            "Mines": 100,
            "Power Plants": 50,
            "Op Centres": 1,
            "Psychic Centres": 1,
            "Barracks": 80
            }
        self.research = {
            "Space Exploration": 0,
            "Terraforming": 0,
            "Lunar Colonies": 0,
            "Superweapons": 0,
            "": 0,
            "": 0
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

    def spare_land(self):
        return self.land - sum(self.buildings.values)
    
    def draftable_pop(self):
        return self.pop * 0.01

    """   
    def get_building_requests(self):
        building_requests = {
            "Houses": int(house_entry.get()),
            "Mines": int(mine_entry.get()),
            "Power Plants": int(pplant_entry.get()),
            "Op Centres": int(opcentre_entry.get()),
            "Psychic Centres": int(psycentre_entry.get()),
            "Barracks": int(barracks_entry.get())  
        }
        return building_requests
    """
        
    def update_buildings(self, build_requests):
        try:
            if sum(build_requests.values) <= self.spare_land() and min(build_requests.values >= 0):
                for key in self.buildings:
                    self.buildings[key] += build_requests[key]
                # refresh window!
            else:
                print("Not enough spare land!")
        except:
            print("Entries must be integers!")

    """
    def get_draft_requests(self):
        draft_requests = {
            "Soldiers": int(soldier_entry.get())
            "Scientists": int(scientist_entry.get())
            "Psychics": int(psychic_entry.get())
            "Operatives": int(operative_entry.get())
        }
        return draft_requests
    """
    def draft_units(self, draft_requests):
        try:
            if sum(draft_requests.values) <= self.draftable_pop() and min(draft_requests.values >= 0):
                for key in self.draft_requests:
                    self.units[key] += draft_requests[key]
                # refresh window!
            else:
                print("Not enough draftable population!")
        except:
            print("Entries must be integers!")



