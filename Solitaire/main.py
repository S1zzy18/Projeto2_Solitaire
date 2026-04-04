#!uv run
# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "flet[all]>=0.81.0",
# ]
# ///

import flet as ft
from settings import Settings
from layout import create_appbar
from solitaire import Solitaire, SOLITAIRE_WIDTH, SOLITAIRE_HEIGHT

def main(page: ft.Page):
    page.bgcolor = ft.Colors.GREEN_800

    def handle_resize(e):
        screen_width = page.width
        screen_height = page.height

        if screen_width and screen_height:
            available_height = screen_height - 80

            scale_w = screen_width / SOLITAIRE_WIDTH
            scale_h = available_height / SOLITAIRE_HEIGHT

            scale_factor = min(scale_w, scale_h, 1.0)
            solitaire.scale = scale_factor
            
            solitaire.alignment = ft.Alignment(-1, -1)
            page.update()
        
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

    page.on_resize = handle_resize
    
    settings = Settings()
    create_appbar(page, settings, on_new_game)

    solitaire = Solitaire(settings, on_win)
    page.add(solitaire)

    page.on_error = lambda e: print("Page error:", e.data)

ft.run(main, assets_dir="assets")