import unittest
from app import db, models

"""
Testing a database with just one game and a few players and card
and if their interactions is working
"""


def createFakeDB():

    # Create a Fake Game
    games = list()
    games.append(models.Game(isOn=True))
    for o in games:
        db.session.add(o)
    db.session.commit()
    print games

    # Create Fake Players
    players = list()
    players.append(models.Player(name='Anna', email='anna.ozbek@gmail.com'))
    players.append(models.Player(name='Selim', email='selimyoussry@gmail.com'))
    players.append(models.Player(name='Volcy', email='volcy1@hotmail.fr'))
    for o in players:
        db.session.add(o)
    db.session.commit()
    print players

    # Add players to the game
    gameplayers = list()
    gameplayers.append(models.GamePlayer(id_game=games[0].id, id_player=players[0].id, points=0))
    gameplayers.append(models.GamePlayer(id_game=games[0].id, id_player=players[1].id, points=5))
    gameplayers.append(models.GamePlayer(id_game=games[0].id, id_player=players[2].id, points=3))
    for o in gameplayers:
        db.session.add(o)
    db.session.commit()
    print gameplayers

    # Give cards to players
    gameplayercards = list()
    gameplayercards.append(models.GamePlayerCard(id_game_player=gameplayers[0].id, id_card=models.Card.query.get(1).id))
    for o in gameplayercards:
        db.session.add(o)
    db.session.commit()
    print gameplayercards

def clearDatabase(objects):

    for o in objects:
        db.session.delete(o)
    db.session.commit()


# Here's our "unit tests".
class BasicDBRelations(unittest.TestCase):

    def testOne(self):
        self.failUnless(1)

    def testTwo(self):
        self.failIf(2)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
