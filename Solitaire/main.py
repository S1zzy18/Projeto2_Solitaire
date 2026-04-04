#!uv run
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "flet[all]>=0.27.3",
# ]
# ///

import flet as ft
from solitaire import Solitaire

def main(page: ft.Page):
    page.on_error = lambda e: print("Page error:", e.data)

    solitaire = Solitaire()

    page.add(solitaire)

ft.run(main, assets_dir="assets")