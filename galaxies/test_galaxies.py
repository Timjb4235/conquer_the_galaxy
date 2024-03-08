import pytest

from game import *

@pytest.fixture
def game():
    return Game("Test Player")

def test_init(game):
    assert game.round == 0
    assert game.phase == 1

def test_spare_land(game):
    # Checking initial spare land is correct
    assert game.player.spare_land() == 188

def test_draftable_pop(game):
    # Checking initial draftable pop value is correct
    assert game.player.draftable_pop == 40

def test_update_buildings_success(game):
    building_possibility = {
        "Houses": 4,
        "Mines": 60,
        "Power Plants": 25,
        "Op Centres": 9,
        "Psychic Centres": 9,
        "Barracks": 20  
    }
    game.player.update_buildings(building_possibility)
    assert game.player.buildings == {
            "Houses": 84,
            "Mines": 160,
            "Power Plants": 75,
            "Op Centres": 10,
            "Psychic Centres": 10,
            "Barracks": 100
            }
    
def test_draft_units_success(game):
    draft_requests = {
            "Soldiers": 5,
            "Scientists": 10,
            "Psychics": 1,
            "Operatives": 3
        }
    game.player.draft_units(draft_requests)
    assert game.player.units["Soldiers"] == 5
    assert game.player.units["Scientists"] == 10
    assert game.player.units["Psychics"] == 1
    assert game.player.units["Operatives"] == 3

    
def test_mission_success(game):
    game.player.units["Operatives"] += 3
    assert game.player.mission_succeeds(1, "Steal") == True
    assert game.player.mission_succeeds(4, "Sabotage Defences") == False

def test_general_return(game):
    unit_division = {"Attackers": 1000, "Elites": 1000}
    game.player.units["Generals"] = 3
    game.player.generals_away.append(GeneralAway(unit_division, 1))
    attackers, elites = game.player.units["Attackers"], game.player.units["Elites"]
    game.player.tick()
    assert game.player.units["Generals"] == 4
    assert game.player.units["Attackers"] >= attackers + 1000
    assert game.player.units["Elites"] >= elites + 1000





