__author__ = 'selim'

import models
import random

INITIAL_N_CARDS_PER_RANK = 4
RANKS = [1, 2, 3]
N_COLOR_TOKENS = 5
N_YELLOW_TOKENS = 5
N_SQUARES = 3


def listify(l):
    return [x for x in l]


class GameSetUp:

    def __init__(self, db, game_id=0, game=None):
        if game is None:
            print 'gameid', game_id
            self.game = models.Game.query.get(game_id)
        else:
            self.game = game
        self.db = db

    def initialize_game(self):
        if self.game.isOn:
            print 'Game already on'
            return False

        self.assign_player_order()
        self.initialize_cards_deck()
        self.initialize_cards_table()
        self.initialize_squares_table()
        self.initialize_tokens_table()
        self.initialize_tokens_players()

        self.game.isOn = True
        self.db.session.commit()

        print 'Game initialized!'

    def assign_player_order(self):
        player_orders = random.sample(self.game.get_players(), len(self.game.get_players()))
        for assigned_order in range(len(player_orders)):
            player_orders[assigned_order].game_order = assigned_order
            player_orders[assigned_order].ismyturntoplay = assigned_order == 0

        self.db.session.commit()

    def initialize_cards_deck(self):
        all_cards_ids = set([card.id for card in models.Card.query.all()])

        for card_id in all_cards_ids:
            game_deck_card_tmp = models.GameDeckCard(
                id_game=self.game.id,
                id_card=card_id)
            self.db.session.add(game_deck_card_tmp)
        self.db.session.commit()
        print 'Cards added to deck'

    def initialize_cards_table(self):
        # Place randomly 4 cards for each color
        deck_cards = models.GameDeckCard.query.filter(models.GameDeckCard.id_game==self.game.id).all()
        deck_cards_per_rank = {1: set(), 2: set(), 3: set()}
        for deck_card in deck_cards:
            deck_cards_per_rank[deck_card.card.rank].add(deck_card)
        for r in RANKS:
            picked_deck_cards = random.sample(deck_cards_per_rank[r], INITIAL_N_CARDS_PER_RANK)
            for deck_card in picked_deck_cards:
                game_table_card_tmp = models.GameTableCard(
                    id_game=self.game.id,
                    id_card=deck_card.card.id
                )
                self.db.session.add(game_table_card_tmp)
                print deck_card
                self.db.session.delete(deck_card)
        self.db.session.commit()
        print 'Cards chosen placed on the table'

    def initialize_squares_table(self):
        table_squares_ids = [square.id for square in models.Square.query.all()]
        picked_squares_ids = random.sample(table_squares_ids, N_SQUARES)

        for square_id in picked_squares_ids:
            table_square_tmp = models.GameTableSquare(
                id_game=self.game.id,
                id_square=square_id
            )
            self.db.session.add(table_square_tmp)
        self.db.session.commit()
        print 'Squares chosen and places on table'

    def initialize_tokens_table(self):
        table_tokens = models.GameTableTokens(
            id_game=self.game.id,
            nblue=N_COLOR_TOKENS,
            nred=N_COLOR_TOKENS,
            ngreen=N_COLOR_TOKENS,
            nblack=N_COLOR_TOKENS,
            nwhite=N_COLOR_TOKENS,
            nyellow=N_YELLOW_TOKENS
        )
        self.db.session.add(table_tokens)
        self.db.session.commit()
        print 'Tokens displayed on the table'

    def initialize_tokens_players(self):
        for id_game_player in [p.id for p in self.game.get_players()]:
            game_player_tokens_tmp = models.GamePlayerTokens(
                id_game_player = id_game_player,
                nblue = 0,
                ngreen = 0,
                nred = 0,
                nblack = 0,
                nwhite = 0,
                nyellow = 0)
            self.db.session.add(game_player_tokens_tmp)
            self.db.session.commit()
        print '0 Token for each player'
