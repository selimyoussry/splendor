__author__ = 'selim'

from app.models import Card, Square, colors
from app import db


def add_cards(rank):

    f = open('cards_rank{}.txt'.format(rank), 'r')

    for line in f:
        card_info = get_card_info(line)
        card = Card(rank=rank,
                    color=card_info['color'],
                    value=card_info['value'],
                    nblack=card_info['nblack'],
                    ngreen=card_info['ngreen'],
                    nwhite=card_info['nwhite'],
                    nred=card_info['nred'],
                    nblue=card_info['nblue']
                    )
        db.session.add(card)
    db.session.commit()


def add_squares():

    f = open('squares.txt', 'r')

    for line in f:
        square_info = get_square_info(line)
        square = Square(nblack=square_info['nblack'],
                    ngreen=square_info['ngreen'],
                    nwhite=square_info['nwhite'],
                    nred=square_info['nred'],
                    nblue=square_info['nblue']
        )
        db.session.add(square)
    db.session.commit()


def get_card_info(line):
    card_info = {'ngreen': 0, 'nwhite': 0, 'nblue': 0, 'nred': 0, 'nblack': 0}

    s = line.split(',')
    card_info['color']= s[0]

    # Get card value
    card_info['value'] = 0
    if 'point' in s[-1]:
        card_info['value'] = int(s[-1].replace('points', ''))
        tokens = set(s[1:-1])
    else:
        tokens = set(s[1:])

    # Needed tokens to buy card
    for token in tokens:
        for color in colors:
            if color in token:
                card_info['n{}'.format(color)] = int(token.replace(color, ''))

    return card_info


def get_square_info(line):
    square_info = {'ngreen': 0, 'nwhite': 0, 'nblue': 0, 'nred': 0, 'nblack': 0}

    tokens = line.split(',')

    # Needed tokens to buy card
    for token in tokens:
        for color in colors:
            if color in token:
                square_info['n{}'.format(color)] = int(token.replace(color, ''))

    return square_info


if __name__ == '__main__':
    for rank in [1, 2, 3]:
        add_cards(rank=rank)
    add_squares()