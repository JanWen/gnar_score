from chalicelib.elo import Elo

def base_test():
    assert 2 + 2 == 4

def test_init_elo():
    elo = Elo()
    assert len(elo.elo) == 673
    assert sum([i.elo for i in elo.elo.values()]) == 673*1000


def test_update_elo():
    elo = Elo()
    blue_team = {
        "id": "109637393694097670",
        "result": {
            "outcome": "win",
            "gameWins": 3
        }
    }
    red_team = {
        "id": "105521706535388095",
        "result": {
            "outcome": "loss",
            "gameWins": 2
        }
    }

    elo.update_elo(blue_team, red_team, "league_id")

    assert elo.elo["109637393694097670"].elo > 1000
    assert elo.elo["105521706535388095"].elo < 1000