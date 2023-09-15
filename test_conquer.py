import pytest
from conquer_the_galaxy import *

@pytest.fixture
def game():
    game = Game()

def test_spare_land(game):
    # Checking initial spare land is correct
    assert game.player.spare_land == 188

def test_draftable_pop(game):
    # Checking initial draftable pop value is correct
    assert game.player.draftable_pop() == 50

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
    
# Use pytest.raises() to check the correct errors occur