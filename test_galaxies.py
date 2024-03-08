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
    assert game.player.units == {
            "Soldiers": 5,
            "Scientists": 10,
            "Psychics": 1,
            "Operatives": 3
        }
    
def test_mission_success(game):
    game.player.units["Operatives"] += 3
    assert game.player.mission_succeeds(1, "Steal") == True
    assert game.player.mission_succeeds(4, "Sabotage Defences") == False




