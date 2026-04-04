#Global constants for the card dimensions and drop proximity
CARD_WIDTH = 70
CARD_HEIGHT = 100
DROP_PROXIMITY = 30
CARD_OFFSET = 20

import flet as ft

class Card(ft.GestureDetector):
    def __init__(self, solitaire, suite, rank):
        super().__init__()
        self.solitaire = solitaire
        self.suite=suite
        self.rank=rank
        self.face_up=False
        self.slot= None
        self.draggable_pile = [self]
        self.top= 0
        self.left= 0
        self.start_top = 0
        self.start_left = 0

        self.mouse_cursor=ft.MouseCursor.MOVE
        self.drag_interval=5
        self.on_pan_start=self.start_drag
        self.on_pan_update=self.drag
        self.on_pan_end=self.drop
        #self.on_tap = self.click
        #self.on_double_tap = self.doubleclick
        self.content=ft.Container(
            bgcolor=ft.Colors.GREEN,
            width= CARD_WIDTH,
            height= CARD_HEIGHT,
            border_radius = ft.border_radius.all(6),
            content=ft.Image(src="/images/card_back.png")
        )
    
    def turn_face_up(self):
        self.face_up = True
        self.content.content.src = f"/images/{self.rank.name}_{self.suite.name}.svg"
        self.solitaire.update()

    def move_on_top(self):
        for card in self.draggable_pile:
            self.solitaire.controls.remove(card)
            self.solitaire.controls.append(card)

    def bounce_back(self):
        for card in self.draggable_pile:
            card.top = card.start_top
            card.left = card.start_left
        self.solitaire.update()

    def place(self, slot):
        for card in self.draggable_pile:
            if slot in self.solitaire.tableau:
                card.top = slot.top + len(slot.pile) * CARD_OFFSET
            else:
                card.top = slot.top
                card.left = slot.left

            if card.slot is not None:
                card.slot.pile.remove(card)

            card.slot = slot

            slot.pile.append(card)

        self.solitaire.update()

    def get_draggable_pile(self):
        if self.slot is not None:
            self.draggable_pile = self.slot.pile[self.slot.pile.index(self) :]
        else:
            self.draggable_pile = [self]

    def start_drag(self, e: ft.DragStartEvent):
        self.get_draggable_pile()
        self.move_on_top()
        self.solitaire.update()

    def drag(self, e: ft.DragUpdateEvent):
        for card in self.draggable_pile:
            card.top = (
                max(0, self.top + e.local_delta.y)
                + self.draggable_pile.index(card) * CARD_OFFSET
            )
            card.left = max(0, self.left + e.local_delta.x)
            self.solitaire.update()

    def drop(self, e: ft.DragEndEvent):
        for slot in self.solitaire.tableau:
            if (
                abs(self.top - (slot.top + len(slot.pile) * CARD_OFFSET))
                < DROP_PROXIMITY
                and abs(self.left - slot.left) < DROP_PROXIMITY
            ):
                self.place(slot)
                self.solitaire.update()
                return
        for slot in self.solitaire.foundations:
            if (
                abs(self.top - slot.top) < DROP_PROXIMITY
                and abs(self.left - slot.left) < DROP_PROXIMITY
            ):
                self.place(slot)
                self.solitaire.update()
                return

        self.bounce_back()