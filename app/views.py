from flask import render_template, flash, redirect
from app import app
from forms import *
import models
from app import db

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
                           title='Home')


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        flash('Signup requested for Name="{}", Email={}'.format(form.name.data, form.email.data))

        # Add the new player to the database
        new_player = models.Player(name=form.name.data, email=form.email.data)
        db.session.add(new_player)
        db.session.commit()

        return redirect('/index')
    return render_template('sign_up.html',
                           title='Sign Up',
                           form=form)


@app.route('/start_game', methods=['GET', 'POST'])
def start_game():
    form = StartGameForm()

    if form.validate_on_submit():

        players_email = [form.player1.data, form.player2.data, form.player3.data, form.player4.data, form.player5.data]
        players_email = [email for email in players_email if len(email) > 0]
        flash('Start a game requested for players {}'.format(' - '.join(players_email)))

        # Instanciate a new game
        new_game = models.Game(isOn=True)
        db.session.add(new_game)
        #db.session.commit()

        # Match players to game
        players = list()
        for player_email in players_email:
            players.extend(models.Player.query.filter(models.Player.email==player_email).all())
            ################## FINISH HERE

        print players

        new_game_id = 10
        return redirect('/game/{}'.format(new_game_id))
    return render_template('start_game.html',
                           title='Start a new game',
                           form=form)


@app.route('/game', methods=['GET', 'POST'])
@app.route('/game/<game_id>', methods=['GET', 'POST'])
def game(game_id=0):

    print 'Game', game_id

    return render_template('game.html',
                           title='Game {}'.format(game_id),
                           game_id=game_id)