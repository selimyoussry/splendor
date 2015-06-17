from forms import *
import models
from initialize_game import GameSetUp
from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from .forms import LoginForm


def listify(l):
    return [x for x in l]


@app.route('/')
@app.route('/index')
@login_required
def index():

    games = models.Game.query.filter(models.Game.isOn==True).all()

    gamesSetUp = [GameSetUp(game=game, db=db) for game in games]

    return render_template('index.html',
                           title='Home',
                           player=g.user,
                           games=gamesSetUp)


@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])

@lm.user_loader
def load_user(id):
    return models.Player.query.get(int(id))

@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = models.Player.query.filter_by(email=resp.email).first()
    if user is None:
        name = resp.nickname
        if name is None or name == "":
            name = resp.email.split('@')[0]
        user = models.Player(name=name, email=resp.email)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))

@app.before_request
def before_request():
    g.user = current_user

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/start_game', methods=['GET', 'POST'])
@login_required
def start_game():
    form = StartGameForm()

    available_players = [p for p in models.Player.query.all()]

    if form.validate_on_submit():

        players_email = [form.player1.data, form.player2.data, form.player3.data, form.player4.data, form.player5.data]
        players_email = [email for email in players_email if len(email) > 0]
        flash('Start a game requested for players {}'.format(' - '.join(players_email)))

        # Instanciate a new game
        new_game = models.Game(isOn=False)
        db.session.add(new_game)
        db.session.commit()

        # Match players to game
        players = list()
        for player_email in players_email:
            players.extend(models.Player.query.filter(models.Player.email==player_email).all())
        players = set(players)

        flash('Only players {} exist'.format(' - '.join([p.email for p in players])))

        for player in players:
            player_game = models.GamePlayer(id_game=new_game.id, id_player=player.id, points=0)
            db.session.add(player_game)
            db.session.commit()
            print 'Adding {}'.format(player_game)

        new_game_id = new_game.id
        return redirect('/game/{}'.format(new_game_id))

    return render_template(url_for('start_game'),
                           title='Start a new game',
                           form=form,
                           available_players=available_players)


@app.route('/game', methods=['GET', 'POST'])
@app.route('/game/<game_id>', methods=['GET', 'POST'])
@login_required
def game(game_id):

    gameSetUp = GameSetUp(
        game_id=game_id,
        db=db
    )

    if not gameSetUp.game.isOn:
        gameSetUp.initialize_game()

    gameplayer = models.GamePlayer.query.filter(models.GamePlayer.id_game == game_id, models.GamePlayer.id_player == g.user.id).all()
    if len(gameplayer) > 0:
        gameplayer = gameplayer[0]

    return render_template('game.html',
                           title='Game {}'.format(game_id),
                           game=gameSetUp.game,
                           gameplayer=gameplayer)



@app.route('/play', methods=['GET', 'POST'])
@login_required
def play():

    gameSetUp = GameSetUp(
        game_id=request.form['game_id'],
        db=db
    )

    print request.form['what']

    if request.form['what'] == 'reserve-a-card':
        gameSetUp.buy_or_reserve_card(
            gameplayer_id=request.form['gameplayer_id'],
            table_card_id=request.form['table_card_id'],
            bought=False
        )
        gameSetUp.play_tokens(
            gameplayer_id=request.form['gameplayer_id'],
            tokens_to_buy='yellow-1'
        )
    elif request.form['what'] == 'buy-a-card':
        gameSetUp.buy_or_reserve_card(
            gameplayer_id=request.form['gameplayer_id'],
            table_card_id=request.form['table_card_id'],
            bought=True
        )
    elif request.form['what'] == 'buy-a-reserved-card':
        print 'trhou'
        gameSetUp.buy_a_reserved_card(
            player_card_id=request.form['player_card_id']
        )
    elif request.form['what'] == 'buy-tokens':
        gameSetUp.play_tokens(
            gameplayer_id=request.form['gameplayer_id'],
            tokens_to_buy=request.form['tokens_to_buy']
        )

    gameSetUp.next_turn()


    return jsonify({'what': request.form['what']})