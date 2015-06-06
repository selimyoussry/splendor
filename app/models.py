__author__ = 'selim'

from app import db

colors = {'white', 'red', 'green', 'blue', 'black'}


class Game(db.Model):
    __tablename__ = 'game'
    id = db.Column(db.Integer, primary_key=True)
    isOn = db.Column(db.Boolean())
    dt = db.Column(db.DateTime, default=db.func.now())

    players = db.relationship('GamePlayer', backref='game', lazy='dynamic')
    table_cards = db.relationship('GameTableCard', backref='game', lazy='dynamic')
    table_squares = db.relationship('GameTableSquare', backref='game', lazy='dynamic')
    table_tokens = db.relationship('GameTableTokens', backref='game', lazy='dynamic')
    deck_cards = db.relationship('GameDeckCard', backref='game', lazy='dynamic')

    def get_players(self):
        return [p for p in self.players]

    def get_table_cards_by_rank(self, rank):
        return [c.card for c in self.table_cards if c.card.rank==rank]

    def get_table_squares(self):
        return [s.square for s in self.table_squares]

    def get_table_tokens(self):
        return self.table_tokens[0]


    def __repr__(self):
        return '<Game {}>'.format(self.id)


class Player(db.Model):
    __tablename__ = 'player'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)

    game_player = db.relationship('GamePlayer', backref='player', lazy='dynamic')

    def __repr__(self):
        return '<Player {} {} {}>'.format(self.id, self.name, self.email)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3


class Card(db.Model):
    __tablename__ = 'card'
    id = db.Column(db.Integer, primary_key=True)
    rank = db.Column(db.Integer)
    color = db.Column(db.String(255))
    value = db.Column(db.Integer)
    nblue = db.Column(db.Integer)
    ngreen = db.Column(db.Integer)
    nwhite = db.Column(db.Integer)
    nred = db.Column(db.Integer)
    nblack = db.Column(db.Integer)

    game_player = db.relationship('GamePlayerCard', backref='card', lazy='dynamic')
    table = db.relationship('GameTableCard', backref='card', lazy='dynamic')
    deck = db.relationship('GameDeckCard', backref='card', lazy='dynamic')

    def get_info(self, color):
        if color == 'blue':
            return self.nblue
        elif color == 'green':
            return self.ngreen
        elif color == 'white':
            return self.nwhite
        elif color == 'black':
            return self.nblack
        elif color == 'red':
            return self.nred

    def __repr__(self):
        return '<{} Card - Yields {} points>'.format(self.color, self.value)


class Square(db.Model):
    __tablename__ = 'square'
    id = db.Column(db.Integer, primary_key=True)
    nblue = db.Column(db.Integer)
    ngreen = db.Column(db.Integer)
    nwhite = db.Column(db.Integer)
    nred = db.Column(db.Integer)
    nblack = db.Column(db.Integer)

    game_player = db.relationship('GamePlayerSquare', backref='square', lazy='dynamic')
    table = db.relationship('GameTableSquare', backref='square', lazy='dynamic')

    def get_info(self, color):
        if color == 'blue':
            return self.nblue
        elif color == 'green':
            return self.ngreen
        elif color == 'white':
            return self.nwhite
        elif color == 'black':
            return self.nblack
        elif color == 'red':
            return self.nred

    def __repr__(self):
        return '<Square - Requires {} blue, {} green, {} white, {} red, {} black>'.format(self.nblue, self.ngreen, self.nwhite, self.nred, self.nblack)


class GamePlayer(db.Model):
    __tablename__ = 'game_player'
    id = db.Column(db.Integer, primary_key=True)
    id_game = db.Column(db.Integer, db.ForeignKey('game.id'))
    id_player = db.Column(db.Integer, db.ForeignKey('player.id'))
    game_order = db.Column(db.Integer)
    points = db.Column(db.Integer)

    cards = db.relationship('GamePlayerCard', backref='gameplayer', lazy='dynamic')
    squares = db.relationship('GamePlayerSquare', backref='gameplayer', lazy='dynamic')
    tokens = db.relationship('GamePlayerTokens', backref='gameplayer', lazy='dynamic')
    turns = db.relationship('GamePlayerTurn', backref='gameplayer', lazy='dynamic')

    def get_cards_by_color(self, color):
        return [c.card for c in self.cards if c.card.color==color and c.bought]

    def get_cards_not_bought(self):
        return [c.card for c in self.cards if not c.bought]

    def get_squares(self):
        return [s.square for s in self.squares]

    def get_tokens(self):
        return self.tokens[0]

    def get_items_per_color(self, color):
        return len(self.get_cards_by_color(color)) + self.get_tokens().get_info(color)

    def get_points(self):
        cards_points = sum([c.card.value for c in self.cards if c.bought])
        squares_points = len(self.get_squares())
        return cards_points + squares_points

    def __repr__(self):
        return '<Game {} - Player {}>'.format(self.game, self.player.name)


class GamePlayerCard(db.Model):
    __tablename__ = 'game_player_card'
    id = db.Column(db.Integer, primary_key=True)
    id_game_player = db.Column(db.Integer, db.ForeignKey('game_player.id'))
    id_card = db.Column(db.Integer, db.ForeignKey('card.id'))
    bought = db.Column(db.Boolean())

    def __repr__(self):
        return '<GamePlayer {} - Card {}>'.format(self.gameplayer, self.card)


class GamePlayerSquare(db.Model):
    __tablename__ = 'game_player_square'
    id = db.Column(db.Integer, primary_key=True)
    id_game_player = db.Column(db.Integer, db.ForeignKey('game_player.id'))
    id_square = db.Column(db.Integer, db.ForeignKey('square.id'))

    def __repr__(self):
        return '<GamePlayer {} - Square {}>'.format(self.gameplayer, self.square)


class GamePlayerTokens(db.Model):
    __tablename__ = 'game_player_tokens'
    id = db.Column(db.Integer, primary_key=True)
    id_game_player = db.Column(db.Integer, db.ForeignKey('game_player.id'))
    nblue = db.Column(db.Integer)
    ngreen = db.Column(db.Integer)
    nred = db.Column(db.Integer)
    nblack = db.Column(db.Integer)
    nwhite = db.Column(db.Integer)
    nyellow = db.Column(db.Integer)

    def get_info(self, color):
        if color == 'blue':
            return self.nblue
        elif color == 'green':
            return self.ngreen
        elif color == 'white':
            return self.nwhite
        elif color == 'black':
            return self.nblack
        elif color == 'red':
            return self.nred
        elif color == 'yellow':
            return self.nyellow

    def __repr__(self):
        return '<GamePlayer {} - NTokens {} blue, {} black, {} red, {} white, {} green, {} yellow>'.format(self.gameplayer, self.nblue, self.nblack, self.nred, self.nwhite, self.ngreen, self.nyellow)


class GameTableCard(db.Model):
    __tablename__ = 'game_table_card'
    id = db.Column(db.Integer, primary_key=True)
    id_game = db.Column(db.Integer, db.ForeignKey('game.id'))
    id_card = db.Column(db.Integer, db.ForeignKey('card.id'))

    def __repr__(self):
        return '<Game {} - Card {}>'.format(self.game, self.card)


class GameTableSquare(db.Model):
    __tablename__ = 'game_table_square'
    id = db.Column(db.Integer, primary_key=True)
    id_game = db.Column(db.Integer, db.ForeignKey('game.id'))
    id_square = db.Column(db.Integer, db.ForeignKey('square.id'))

    def __repr__(self):
        return '<Game {} - Square {}>'.format(self.game, self.square)


class GameTableTokens(db.Model):
    __tablename__ = 'game_table_tokens'
    id = db.Column(db.Integer, primary_key=True)
    id_game = db.Column(db.Integer, db.ForeignKey('game.id'))
    nblue = db.Column(db.Integer)
    ngreen = db.Column(db.Integer)
    nred = db.Column(db.Integer)
    nblack = db.Column(db.Integer)
    nwhite = db.Column(db.Integer)
    nyellow = db.Column(db.Integer)

    def get_info(self, color):
        if color == 'blue':
            return self.nblue
        elif color == 'green':
            return self.ngreen
        elif color == 'white':
            return self.nwhite
        elif color == 'black':
            return self.nblack
        elif color == 'red':
            return self.nred
        elif color == 'yellow':
            return self.nyellow

    def __repr__(self):
        return '<Game {} - NTokens {} blue, {} black, {} red, {} white, {} green, {} yellow>'.format(self.game, self.nblue, self.nblack, self.nred, self.nwhite, self.ngreen, self.nyellow)


class GameDeckCard(db.Model):
    __tablename__ = 'game_deck_card'
    id = db.Column(db.Integer, primary_key=True)
    id_game = db.Column(db.Integer, db.ForeignKey('game.id'))
    id_card = db.Column(db.Integer, db.ForeignKey('card.id'))

    def __repr__(self):
        return '<Game {} - Card {}>'.format(self.game, self.card)


class GamePlayerTurn(db.Model):
    __tablename__ = 'game_turn'
    id = db.Column(db.Integer, primary_key=True)
    id_game_player = db.Column(db.Integer, db.ForeignKey('game_player.id'))

    def __repr__(self):
        return '<GamePlayer {}>'.format(self.gameplayer)