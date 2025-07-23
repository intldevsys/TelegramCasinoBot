import random
from dataclasses import dataclass, field
from typing import List

@dataclass
class Card:
    suit: str
    rank: str
    @property
    def value(self):
        if self.rank in ['J', 'Q', 'K']:
            return 10
        if self.rank == 'A':
            return 11
        return int(self.rank)

@dataclass
class Hand:
    cards: List[Card] = field(default_factory=list)
    @property
    def value(self):
        value = sum(card.value for card in self.cards)
        aces = sum(1 for card in self.cards if card.rank == 'A')
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value
    def is_blackjack(self):
        return self.value == 21 and len(self.cards) == 2

class FairBlackjackGame:
    def __init__(self):
        self.payout_blackjack = 2.5
        self.payout_win = 2.0
    def _create_deck(self):
        suits = ['♠️', '♥️', '♦️', '♣️']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        deck = [Card(s, r) for s in suits for r in ranks]
        random.shuffle(deck)  # <-- Proven random shuffle
        return deck
    def start_hand(self):
        deck = self._create_deck()
        player = Hand([deck.pop(), deck.pop()])
        dealer = Hand([deck.pop(), deck.pop()])
        return player, dealer, deck
    def play_dealer(self, hand, deck):
        while hand.value < 17:
            hand.cards.append(deck.pop())
        return hand
    def result(self, player, dealer):
        if player.value > 21:
            return 'dealer_wins'
        if dealer.value > 21:
            return 'player_wins'
        if player.is_blackjack() and not dealer.is_blackjack():
            return 'player_blackjack'
        if player.value == dealer.value:
            return 'push'
        if player.value > dealer.value:
            return 'player_wins'
        return 'dealer_wins'
