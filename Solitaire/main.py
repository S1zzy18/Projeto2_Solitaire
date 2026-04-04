#!uv run
# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "flet[all]==0.27.3",
# ]
# ///

import flet as ft
from solitaire import Solitaire
from settings import Settings
from layout import create_appbar

def main(page: ft.Page):
    def on_new_game(settings):
        page.controls.pop()
        new_solitaire = Solitaire(settings, on_win)
        page.add(new_solitaire)
        page.update()

    def on_win():
        page.add(
            ft.AlertDialog(
                title=ft.Text("YOU WIN!"),
                open=True,
                on_dismiss=lambda e: page.controls.pop(),
            )
        )
        print("You win")
        page.update()

    settings = Settings()
    create_appbar(page, settings, on_new_game)

    solitaire = Solitaire(settings, on_win)
    page.add(solitaire)

    page.on_error = lambda e: print("Page error:", e.data)

ft.app(main, assets_dir="assets")