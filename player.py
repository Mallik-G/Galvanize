import random


class Player(object):
    def __init__(self, name, dollars=4):
        self.name = name
        self.hand = []
        self.wallet = dollars

    def dealt_cards(self, cards):
        self.hand.append(cards)

    def add_card(self, card):
        self.hand.extend(card)

    def __repr__(self):
        return self.name

    def __len__(self):
        return len(self.hand) + len(self.discard)
