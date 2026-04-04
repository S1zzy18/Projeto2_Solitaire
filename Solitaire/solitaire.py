#Global constants for the solitaire game
SOLITAIRE_WIDTH = 1000
SOLITAIRE_HEIGHT = 500
CARD_OFFSET = 20

import flet as ft
import random

from card import Card
from slot import Slot

class Suite:
    def __init__(self, suite_name, suite_color):
        self.name = suite_name
        self.color = suite_color


class Rank:
    def __init__(self, card_name, card_value):
        self.name = card_name
        self.value = card_value

class Solitaire(ft.Stack):
    def __init__(self, settings, on_win):
        super().__init__()
        self.controls = []
        self.width = SOLITAIRE_WIDTH
        self.height = SOLITAIRE_HEIGHT
        self.current_top = 0
        self.current_left = 0
        self.card_offset = CARD_OFFSET
        self.settings = settings
        self.deck_passes_remaining = int(self.settings.deck_passes_allowed)
        self.controls = []
        self.on_win = on_win
    
    def did_mount(self):
        self.create_card_deck()
        self.create_slots()
        self.deal_cards()
        

    def create_card_deck(self):
        suites = [
            Suite("hearts", "RED"),
            Suite("diamonds", "RED"),
            Suite("clubs", "BLACK"),
            Suite("spades", "BLACK"),
        ]
        ranks = [
            Rank("Ace", 1),
            Rank("2", 2),
            Rank("3", 3),
            Rank("4", 4),
            Rank("5", 5),
            Rank("6", 6),
            Rank("7", 7),
            Rank("8", 8),
            Rank("9", 9),
            Rank("10", 10),
            Rank("Jack", 11),
            Rank("Queen", 12),
            Rank("King", 13),
        ]

        self.cards = []

        for suite in suites:
            for rank in ranks:
                self.cards.append(Card(solitaire=self, suite=suite, rank=rank))

    def create_slots(self):

        self.stock = Slot(solitaire=self, slot_type="stock", top=0, left=0, border=ft.border.all(1))
        self.waste = Slot(solitaire=self, slot_type="waste", top=0, left=100, border=None)

        self.foundations = []

        x = 300
        for i in range(4):
            self.foundations.append(Slot(solitaire=self, slot_type="foundation", top=0, left=x, border=ft.border.all(1, "outline"),))
            x += 100

        self.tableau = []

        x = 0
        for i in range(7):
            self.tableau.append(Slot(solitaire=self, slot_type="tableau", top=150, left=x, border=None,))
            x += 100

        self.controls.append(self.stock)
        self.controls.append(self.waste)
        self.controls.extend(self.foundations)
        self.controls.extend(self.tableau)
        self.update()

    def deal_cards(self):
        random.shuffle(self.cards)
        self.controls.extend(self.cards)

        first_slot = 0
        remaining_cards = self.cards

        while first_slot < len(self.tableau):
            for slot in self.tableau[first_slot:]:
                top_card = remaining_cards[0]
                top_card.place(slot)
                remaining_cards.remove(top_card)
            first_slot += 1


        for card in remaining_cards:
            card.place(self.stock)

        self.update()

        for slot in self.tableau:
            slot.get_top_card().turn_face_up()

        self.update()

    def move_on_top(self, cards_to_drag):
        for card in cards_to_drag:
            self.controls.remove(card)
            self.controls.append(card)
        self.update()

    def bounce_back(self, cards):
        i = 0
        for card in cards:
            card.top = self.current_top
            if card.slot.type == "tableau":
                card.top += i * self.card_offset
            card.left = self.current_left
            i += 1

    def display_waste(self):
        for card in self.waste.pile:
            card.visible = False

        visible_cards = self.waste.get_top_three_cards()

        for i, card in enumerate(visible_cards):
            card.visible = True

            if card in self.controls:
                self.controls.remove(card)
            self.controls.append(card)

            if int(self.settings.waste_size) == 3:
                card.left = self.waste.left + (i * self.card_offset)
            else:
                card.left = self.waste.left

            card.top = self.waste.top
        self.update()

    def restart_stock(self):
        self.waste.pile.reverse()
        while len(self.waste.pile) > 0:
            card = self.waste.pile[0]
            card.turn_face_down()
            card.place(self.stock)
        self.update()

    def check_foundation_rules(self, current_card, top_card=None):
        if top_card is not None:
            return (
                current_card.suite.name == top_card.suite.name
                and current_card.rank.value - top_card.rank.value == 1
            )
        else:
            return current_card.rank.name == "Ace"

    def check_tableau_rules(self, current_card, top_card=None):
        if top_card is not None:
            return (
                current_card.suite.color != top_card.suite.color
                and top_card.rank.value - current_card.rank.value == 1
            )
        else:
            return current_card.rank.name == "King"

    def check_if_you_won(self):
        cards_num = 0
        for slot in self.foundations:
            cards_num += len(slot.pile)
        if cards_num == 52:
            return True
        return False
