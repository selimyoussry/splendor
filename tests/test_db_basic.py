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

    # Create Fake Players
    players = list()
    players.append(models.Player(name='Anna'))
    players.append(models.Player(name='Selim'))
    players.append(models.Player(name='Volcy'))

    # Create Fake Cards
    cards = list()
    cards.append(models.Card(rank=3, color=2, value=3, nblue=3, ngreen=0, nwhite=5, nred=3, nblack=3))
    cards.append(models.Card(rank=2, color=13, value=2, nblue=0, ngreen=5, nwhite=0, nred=3, nblack=0))

    # Create Fake Squares
    squares = list()
    squares.append(models.Square(nblue=4, ngreen=0, nwhite=4, nred=0, nblack=0))
    squares.append(models.Square(nblue=0, ngreen=0, nwhite=4, nred=0, nblack=4))

    # Add players to the game
    gameplayers = list()
    gameplayers.append(models.GamePlayer(id_game=games[0].id, id_player=players[0].id, points=0))
    gameplayers.append(models.GamePlayer(id_game=games[0].id, id_player=players[1].id, points=5))
    gameplayers.append(models.GamePlayer(id_game=games[0].id, id_player=players[2].id, points=3))

    # Give cards to players
    gameplayecards = list()
    gameplayecards

    # Store the db_objects in one list
    db_objects = list()
    db_objects.extend(games)
    db_objects.extend(players)
    db_objects.extend(players)


    # Add them all to the database
    for o_group in db_objects:
        for o in o_group:
            db.session.add(o)
    db.session.commit()

    return [db_objects]


def clearDatabase(objects):

    for o in objects:
        db.session.delete(o)
    db.session.commit()


# Here's our "unit tests".
class BasicDBRelations(unittest.TestCase):

    def testOne(self):
        self.failUnless(IsOdd(1))

    def testTwo(self):
        self.failIf(IsOdd(2))


def main():
    unittest.main()


if __name__ == '__main__':
    main()
