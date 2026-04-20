import flet as ft
import time
from settings import SettingsDialog

rules_md = ft.Markdown(
        """
    Klondike is played with a standard 52-card deck, without Jokers.

    The four foundations (light rectangles in the upper right of the figure) are built up by suit from Ace (low in this game) to King, and the tableau piles can be built down by alternate colors. Every face-up card in a partial pile, or a complete pile, can be moved, as a unit, to another tableau pile on the basis of its highest card. Any empty piles can be filled with a King, or a pile of cards with a King. The aim of the game is to build up four stacks of cards starting with Ace and ending with King, all of the same suit, on one of the four foundations, at which time the player would have won. There are different ways of dealing the remainder of the deck from the stock to the waste, which can be selected in the Settings:

    - Turning three cards at once to the waste, with no limit on passes through the deck.
    - Turning three cards at once to the waste, with three passes through the deck.
    - Turning one card at a time to the waste, with three passes through the deck.
    - Turning one card at a time to the waste, with no limit on passes through the deck.

    If the player can no longer make any meaningful moves, the game is considered lost.
        """
    )

rules_dialog = ft.AlertDialog(
    title=ft.Text("Solitaire rules"),
    content=ft.Container(
        width=520,
        content=ft.ListView(
            controls=[rules_md],
            spacing=8,
            padding=10,
            height=480,
        ),
        padding=0,
    ),
    on_dismiss=lambda e: print("Dialog dismissed!"),
)

def create_appbar(page, settings, on_new_game, solitaire, trigger_bsod):
    solitaire.timer_text = ft.Text("00:00", weight=ft.FontWeight.BOLD)
    solitaire.score_text = ft.Text("Score: 0", weight=ft.FontWeight.BOLD)
    solitaire.moves_text = ft.Text("Moves: 0", weight=ft.FontWeight.BOLD)

    if rules_dialog not in page.overlay:
        page.overlay.append(rules_dialog)

    click_state = {"count": 0, "last_time": 0}

    def handle_score_click(e):
        now = time.time()
        if now - click_state["last_time"] > 0.5:
            click_state["count"] = 1
        else:
            click_state["count"] += 1
        
        click_state["last_time"] = now

        if click_state["count"] == 3:
            trigger_bsod(page, solitaire)

    def new_game_clicked(e):
        on_new_game(settings)

    def show_rules(e):
        page.dialog = rules_dialog
        rules_dialog.open = True
        page.update()

    def show_settings(e):
        settings_dialog = SettingsDialog(settings, on_new_game)
        page.overlay.append(settings_dialog)
        page.dialog = settings_dialog
        settings_dialog.open = True
        page.update()

    score_clicker = ft.GestureDetector(
        content=solitaire.score_text,
        on_tap=handle_score_click,
    )

    page.appbar = ft.AppBar(
        leading=ft.Image(src="/images/card.png"),
        leading_width=30,
        title=ft.Text("Flet solitaire"),
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        actions=[
            ft.Icon(ft.Icons.TIMER_OUTLINED, size=20),
            solitaire.timer_text,
            ft.VerticalDivider(),
            ft.Icon(ft.Icons.STARS_OUTLINED, size=20),
            score_clicker,
            ft.VerticalDivider(),
            ft.Icon(ft.Icons.LEADERBOARD_OUTLINED, size=20),
            solitaire.moves_text,

            ft.IconButton(icon=ft.Icons.SAVE_OUTLINED, tooltip="Save Game", on_click=lambda e: solitaire.save_game()),
            ft.IconButton(icon=ft.Icons.FILE_OPEN_OUTLINED, tooltip="Load Game", on_click=lambda e: solitaire.load_game()),
            ft.IconButton(icon=ft.Icons.UNDO, on_click=lambda e: solitaire.undo_move(), tooltip="Undo last move"),
            ft.IconButton(icon=ft.Icons.RESTART_ALT, on_click=lambda e: solitaire.restart_game(), tooltip="Restart this deck"),
            
            ft.TextButton(content="New game", on_click=new_game_clicked),
            ft.TextButton(content="Rules", on_click=show_rules),
            ft.IconButton(ft.Icons.SETTINGS, on_click=show_settings),
        ],
    )

