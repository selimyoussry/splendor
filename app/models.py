__author__ = 'selim'

from app import db

colors = {0: 'Yellow', 1: 'Blue', 2: 'Green', 3: 'Black', 4: 'Red', 5: 'White'}


class Game(db.Model):
    __tablename__ = 'game'
    id = db.Column(db.Integer, primary_key=True)
    isOn = db.Column(db.Boolean())

    players = db.relationship('GamePlayer', backref='game', lazy='dynamic')

    def __repr__(self):
        return '<Game {}>'.format(self.id)


class Player(db.Model):
    __tablename__= 'player'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    game = db.relationship('GamePlayer', backref='player', lazy='dynamic')

    def __repr__(self):
        return '<Player {} {} >'.format(self.id, self.name)


class Card(db.Model):
    __tablename__ = 'card'
    id = db.Column(db.Integer, primary_key = True)
    rank = db.Column(db.Integer)
    color = db.Column(db.Integer)
    value = db.Column(db.Integer)
    nblue = db.Column(db.Integer)
    ngreen = db.Column(db.Integer)
    nwhite = db.Column(db.Integer)
    nred = db.Column(db.Integer)
    nblack = db.Column(db.Integer)

    def __repr__(self):
        return '<{} Card - Yields {} points>'.format(colors[self.color], self.value)


class Square(db.Model):
    __tablename__ = 'square'
    id = db.Column(db.Integer, primary_key = True)
    nblue = db.Column(db.Integer)
    ngreen = db.Column(db.Integer)
    nwhite = db.Column(db.Integer)
    nred = db.Column(db.Integer)
    nblack = db.Column(db.Integer)

    def __repr__(self):
        return '<Square - Requires {} blue, {} green, {} white, {} red, {} black>'.format(self.nblue, self.ngreen, self.nwhite, self.nred, self.nblack)


class GamePlayer(db.Model):
    __tablename__ = 'game_player'
    id_game = db.Column(db.Integer, db.ForeignKey('game.id'))
    id_player = db.Column(db.Integer, db.ForeignKey('player.id'))
    points = db.Column(db.Integer)

    def __repr__(self):
        return '<Worker %r - %r>' % (self.name, self.job)