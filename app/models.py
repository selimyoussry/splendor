__author__ = 'selim'

from app import db

colors = {'white', 'red', 'green', 'blue', 'black'}


class Game(db.Model):
    __tablename__ = 'game'
    id = db.Column(db.Integer, primary_key=True)
    isOn = db.Column(db.Boolean())
    dt = db.Column(db.DateTime, default=db.func.now())

    players = db.relationship('GamePlayer', backref='game', lazy='dynamic')

    def __repr__(self):
        return '<Game {}>'.format(self.id)


class Player(db.Model):
    __tablename__ = 'player'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)

    game = db.relationship('GamePlayer', backref='player', lazy='dynamic')

    def __repr__(self):
        return '<Player {} {} {}>'.format(self.id, self.name, self.email)


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

    game_player_card = db.relationship('GamePlayerCard', backref='card', lazy='dynamic')

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

    def __repr__(self):
        return '<Square - Requires {} blue, {} green, {} white, {} red, {} black>'.format(self.nblue, self.ngreen, self.nwhite, self.nred, self.nblack)


class GamePlayer(db.Model):
    __tablename__ = 'game_player'
    id = db.Column(db.Integer, primary_key=True)
    id_game = db.Column(db.Integer, db.ForeignKey('game.id'))
    id_player = db.Column(db.Integer, db.ForeignKey('player.id'))
    points = db.Column(db.Integer)

    game_player_cards = db.relationship('GamePlayerCard', backref='gameplayer', lazy='dynamic')

    def __repr__(self):
        return '<Game {} - Player {}>'.format(self.game, self.player.name)


class GamePlayerCard(db.Model):
    __tablename__ = 'game_player_card'
    id = db.Column(db.Integer, primary_key=True)
    id_game_player = db.Column(db.Integer, db.ForeignKey('game_player.id'))
    id_card = db.Column(db.Integer, db.ForeignKey('card.id'))

    def __repr__(self):
        return '<GamePlayer {} - Card {}>'.format(self.gameplayer, self.card)