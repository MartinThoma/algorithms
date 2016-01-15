#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""An example implementation for a card game."""

__author__ = "Martin Thoma"
__copyright__ = "I dont care"
__credits__ = ["Martin Thoma"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Martin Thoma"
__email__ = "info@martin-thoma.de"
__status__ = "Prototype"

from random import shuffle, sample
from copy import deepcopy


class Card(object):
    """A single card, e.g. 'Ace of Spades'."""
    def __init__(self, suit, rank, name=""):
        self.suit = suit
        self.rank = rank
        self.name = name

    def __eq__(self, other):
        return self.suit == other.suit \
            and self.rank == other.rank \
            and self.name == other.name

    def __str__(self):
        return self.name

    def __repr__(self):
        if self.name != str(self.rank):
            return "%s %s (%s)" % (str(self.rank), self.suit, self.name)
        else:
            return "%s %s" % (str(self.rank), self.suit)


class CardSet(object):
    """Some cards."""

    def __init__(self, name):
        self.cards = []
        self.name = name

    def shuffle(self):
        """Shuffle the cards of this card set."""
        shuffle(self.cards)

    def append(self, card):
        """Add a card to the card set."""
        self.cards.append(card)

    def draw(self):
        """
        Draw a card from the card set.

        This removes the card from it.
        """
        return self.cards.pop()

    def __str__(self):
        return "%s[%s]" % (self.name, self.cards)

    def __iter__(self):
        for card in self.cards:
            yield card

    def __getitem__(self, key):
        return self.cards[key]


class CardGame(object):
    """
    Parameters
    ----------
    name : str
    players : int
    deck : Deck object
    """
    def __init__(self, name, players, deck):
        self.name = name
        self.players = players
        self.deck = deck
        self.hands = {}
        for player in players:
            self.hands[player] = CardSet(player + "s Cards")

    def deal(self, num_cards=7):
        """Give every player `num_cards` cards."""
        self.deck.shuffle()
        for player in self.players:
            for i in range(num_cards):
                self.hands[player].append(self.deck.draw())

    def does_player_have_card(self, player, card):
        """
        Check if `player` has `card` on his hand.

        Parameters
        ----------
        player : int
        card : object

        Returns
        -------
        bool
        """
        return card in self.hands[player]

    def __str__(self):
        s = self.name + ":\n"
        for player in self.players:
            s += "\t" + str(self.hands[player]) + "\n"
        return s

    def __repr__(self):
        if self.name != str(self.rank):
            return "%s %s (%s)" % (str(self.rank), self.suit, self.name)
        else:
            return "%s %s" % (str(self.rank), self.suit)

if __name__ == "__main__":
    players = ["Martin", "Marie", "Tobi", "Ina"]

    """Initialise french card set."""
    suits = ["Clubs", "Diamonds", "Heart", "Spades"]
    names_values = [["7", 7],
                    ["8", 8],
                    ["9", 9],
                    ["10", 10],
                    ["Jack", 10],
                    ["Queen", 10],
                    ["King", 10],
                    ["Ace", 11]]
    french_deck = CardSet("French Deck")
    for suit in suits:
        for name, value in names_values:
            new_card = Card(suit, value, name)
            french_deck.append(new_card)

    """Initialise german card set."""
    suits = ["Schellen", "Heart", "Gras", "Eichel"]
    names_values = [["7", 7],
                    ["8", 8],
                    ["9", 9],
                    ["10", 10],
                    ["Unter", 2],
                    ["Ober", 3],
                    ["King", 4],
                    ["Ace", 11]]
    german_deck = CardSet("German Deck")
    for suit in suits:
        for name, value in names_values:
            new_card = Card(suit, value, name)
            german_deck.append(new_card)

    print("#"*80)
    schafkopf = CardGame("Schafkopf", players, german_deck)
    schafkopf.deal(8)
    print(schafkopf)
    print(schafkopf.deck)

    print("#"*80)
    skat = CardGame("Skat", players[0:3], deepcopy(french_deck))
    skat.deal(10)
    print(skat.does_player_have_card(players[0], french_deck[10]))
    print(skat.does_player_have_card(players[1], french_deck[10]))
    print(skat.does_player_have_card(players[2], french_deck[10]))
    print(schafkopf)
    print(schafkopf.deck)
