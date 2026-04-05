#Global constants for the solitaire game
SOLITAIRE_WIDTH = 900
SOLITAIRE_HEIGHT = 600
CARD_OFFSET = 40

import flet as ft
import random
import json

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

        self.scale = 1.0
        self.animate_scale = ft.Animation(300, ft.AnimationCurve.DECELERATE)
        self.clip_behavior = ft.ClipBehavior.NONE

        self.current_top = 0
        self.current_left = 0
        self.card_offset = CARD_OFFSET
        self.settings = settings
        self.deck_passes_remaining = int(self.settings.deck_passes_allowed)
        self.controls = []
        self.on_win = on_win

        self.history = []
        self.original_order = []
    
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
        self.stock = Slot(solitaire=self, slot_type="stock", top=0, left=0, border=ft.Border.all(1))
        self.waste = Slot(solitaire=self, slot_type="waste", top=0, left=100, border=None)

        self.foundations = []

        x = 375
        for i in range(4):
            slot = Slot(solitaire=self, slot_type="foundation", top=0, left=x, border=ft.Border.all(1, "outline"),)
            slot.name = f"foundation_{i}"
            self.foundations.append(slot)
            x += 125

        self.tableau = []

        x = 0
        for i in range(7):
            slot = Slot(solitaire=self, slot_type="tableau", top=190, left=x, border=None,)
            slot.name = f"tableau_{i}"
            self.tableau.append(slot)
            x += 125

        self.stock.name = "stock"
        self.waste.name = "waste"

        for i, slot in enumerate(self.foundations):
            slot.name = f"foundation_{i}"

        for i, slot in enumerate(self.tableau):
            slot.name = f"tableau_{i}"

        self.controls.append(self.stock)
        self.controls.append(self.waste)
        self.controls.extend(self.foundations)
        self.controls.extend(self.tableau)
        self.update()

    def deal_cards(self):
        random.shuffle(self.cards)
        self.original_order = list(self.cards)
        self.controls.extend(self.cards)
        remaining_cards = list(self.cards)

        first_slot = 0

        while first_slot < len(self.tableau):
            for slot in self.tableau[first_slot:]:
                top_card = remaining_cards[0]
                top_card.place(slot)
                remaining_cards.remove(top_card)
            first_slot += 1


        for card in remaining_cards:
            card.place(self.stock, False)

        self.update()

        for slot in self.tableau:
            slot.get_top_card().turn_face_up(False)

        self.update()

    def move_on_top(self, cards_to_drag, update=True):
        for card in cards_to_drag:
            if card in self.controls:
                self.controls.remove(card)
            self.controls.append(card)
        if update:
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
        if len(self.waste.pile) > 0:
            self.record_move(self.waste.pile[:], self.waste, self.stock)
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
    
    def record_move(self, cards, source_slot, destination_slot, revealed_card=None):
        move = {
            "cards": list(cards), 
            "from": source_slot,
            "to": destination_slot,
            "revealed": revealed_card 
        }
        self.history.append(move)
        print(f"Move Recorded! History size: {len(self.history)}")

    def undo_move(self, update=True):
        if not self.history:
            print("No moves to undo!")
            return
        
        last_move = self.history.pop()
        
        if last_move["revealed"]:
            last_move["revealed"].turn_face_down()

        for card in last_move["cards"]:
            card.place(last_move["from"], False)

        if last_move["from"].type == "stock":
            card.turn_face_down()
            card.left = last_move["from"].left
            card.top = last_move["from"].top
            card.visible = True

        if last_move["from"].type == "waste" or last_move["to"].type == "waste":
            self.display_waste()
        
        self.update()

    def restart_game(self, update=True):
        if not self.history:
            return
        while len(self.history) > 0:
            self.undo_move(False)
        if update:
            self.update()

    def save_game(self):
        save_data = {
            "original_order": [card.id for card in self.original_order],
            "history": []
        }
        for move in self.history:
            revealed_id = move["revealed"].id if move["revealed"] else None
            move_data = {
                "card_ids": [c.id for c in move["cards"]],
                "from": move["from"].name,
                "to": move["to"].name,
                "revealed_id": revealed_id
            }
            save_data["history"].append(move_data)

        with open("save_game.json", "w") as f:
            json.dump(save_data, f, indent=4)
        print("Game Saved!")

    def load_game(self):
        try:
            with open("save_game.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            print("No save found!")
            return
        
        print(f"Current Deck Size: {len(self.cards)}")
        # print(f"Available IDs: {list(id_map.keys())[:5]}...")
        
        id_map = {card.id: card for card in self.cards}


        missing_ids = []
        for card_id in data["original_order"]:
            clean_id = card_id.strip().lower()
            if clean_id not in id_map:
                missing_ids.append(clean_id)
        
        if missing_ids:
            print(f"FATAL ERROR: The following cards are missing from the current deck: {missing_ids}")
            print(f"First 10 IDs in memory: {list(id_map.keys())[:10]}")
            return

        self.original_order = [id_map[card_id.strip().lower()] for card_id in data["original_order"]]

        for slot in [self.stock, self.waste] + self.tableau + self.foundations:
            slot.pile.clear()

        self.history = []
        temp_cards = list(self.original_order)
        
        first_slot = 0
        while first_slot < len(self.tableau):
            for slot in self.tableau[first_slot:]:
                top_card = temp_cards.pop(0)
                top_card.place(slot, update=False)
                top_card.turn_face_down() # Reset to face down
            first_slot += 1

        for card in temp_cards:
            card.place(self.stock, update=False)
            card.turn_face_down()

        for slot in self.tableau:
            if slot.pile:
                slot.get_top_card().turn_face_up()

        all_slots = {s.name: s for s in [self.stock, self.waste] + self.tableau + self.foundations}

        for move in data["history"]:
            cards_to_move = [id_map[c_id] for c_id in move["card_ids"]]
            dest_slot = all_slots[move["to"]]
            source_slot = all_slots[move["from"]]

            for card in cards_to_move:
                card.place(dest_slot, False)
                if dest_slot.type == "waste":
                    card.turn_face_up()
                elif dest_slot.type == "stock":
                    card.turn_face_down()

            revealed_card = None
            if move["revealed_id"]:
                revealed_card = id_map[move["revealed_id"]]
                revealed_card.turn_face_up()
            self.record_move(cards_to_move, source_slot, dest_slot, revealed_card)

        self.display_waste()
        self.controls = [self.stock, self.waste] + self.foundations + self.tableau + self.cards
        self.update()
        print("Game Loaded!")
        