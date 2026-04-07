#!uv run
# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "flet[all]>=0.81.0",
# ]
# ///

import flet as ft
import time
import threading

from settings import Settings
from layout import create_appbar
from solitaire import Solitaire, SOLITAIRE_WIDTH, SOLITAIRE_HEIGHT

def main(page: ft.Page):
    page.bgcolor = ft.Colors.GREEN_800
    page.padding = 0
    page.spacing = 0

    def trigger_bsod(page, solitaire):
        solitaire.stop_timer()
        
        bsod_layout = ft.Container(
            expand=True,
            bgcolor="#0078D7", # Azul clássico do Windows
            padding=ft.padding.all(50),
            content=ft.Column([ft.Text(":(", size=120, color=ft.Colors.WHITE, weight=ft.FontWeight.W_400),
                ft.Text("O seu jogo de Solitário deparou-se com um problema e precisa de ser reiniciado.",
                    size=30, color=ft.Colors.WHITE, weight=ft.FontWeight.W_300
                ),ft.Text("Estamos apenas a recolher algumas informações de erro (0% concluído).",
                    size=20, color=ft.Colors.WHITE
                ),ft.Container(height=40),
                ft.Row([
                    ft.Image(
                        src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=https://flet.dev", 
                        width=120
                    ), ft.Column([
                        ft.Text("Para mais informações sobre este erro, visite:", color=ft.Colors.WHITE, size=14),
                        ft.Text("https://flet.dev/docs/controls/gesturedetector", color=ft.Colors.WHITE, size=14),
                        ft.Text("Stop Code: SCORE_CLICK_OVERFLOW", color=ft.Colors.WHITE, size=12, weight=ft.FontWeight.BOLD),
                    ], spacing=5)], vertical_alignment=ft.CrossAxisAlignment.START)], spacing=20, alignment=ft.MainAxisAlignment.CENTER)
        )

        page.controls.clear()
        page.appbar = None
        page.bgcolor = "#0078D7"
        page.add(bsod_layout)
        page.update()

    def update_stats():
        # Atualiza os textos da AppBar com os dados do objeto solitaire
        if solitaire and hasattr(solitaire, "timer_text"):
            mins, secs = divmod(solitaire.seconds_elapsed, 60)
            solitaire.timer_text.value = f"{mins:02d}:{secs:02d}"
            solitaire.score_text.value = f"Score: {solitaire.score}"
            solitaire.moves_text.value = f"Moves: {len(solitaire.history)}"
            page.update()

    def tick_timer():
        while True:
            if solitaire.timer_running:
                solitaire.seconds_elapsed += 1
                update_stats()
            time.sleep(1)

    def handle_resize(e):
        if page.width and page.height:
            # Desconto do espaço da appbar
            available_height = page.height - 40 

            scale_w = page.width / SOLITAIRE_WIDTH
            scale_h = available_height / SOLITAIRE_HEIGHT

           
            scale_factor = min(scale_w, scale_h, 1.0)
            solitaire.scale = scale_factor
            
            
            if page.platform == ft.PagePlatform.IOS:
               
                solitaire.offset = ft.Offset(-0.1, -0.2) 
                solitaire.alignment = ft.Alignment(-1, -1)
            else:
              
                solitaire.offset = ft.Offset(0, 0) 
                solitaire.alignment = ft.Alignment(0, 0)
                
            page.update()
        
    def on_new_game(new_settings):
        nonlocal solitaire
        
        # Limpa o jogo anterior
        if len(page.controls) > 0:
            page.controls.pop()
            
        # Cria a nova instância com as settings escolhidas
        new_solitaire = Solitaire(new_settings, on_win)
        
        # Atualizamos a referência para o handle_resize saber quem controlar
        solitaire = new_solitaire
        solitaire.on_stats_change = update_stats
        
        create_appbar(page, settings, on_new_game, solitaire, trigger_bsod)
        page.appbar.actions[0].on_click = lambda e: solitaire.save_game()
        page.appbar.actions[1].on_click = lambda e: solitaire.load_game()
        page.appbar.actions[2].on_click = lambda e: solitaire.undo_move()
        page.appbar.actions[3].on_click = lambda e: solitaire.restart_game()

        # Envolve o jogo num ListView para permitir scroll quando não couber na janela
        game_view = ft.Container(
            expand=True,
            content=ft.ListView(
                controls=[ft.Container(content=solitaire, width=SOLITAIRE_WIDTH, height=SOLITAIRE_HEIGHT)],
                expand=True,
                spacing=0,
                padding=0,
            ),
        )
        page.add(game_view)
        solitaire.start_timer()
        # Forçamos o redimensionamento para aplicar os offsets da plataforma
        handle_resize(None)
        

    def on_win():
        page.dialog = ft.AlertDialog(title=ft.Text("YOU WIN!"))
        page.dialog.open = True
        page.update()

    # Define o evento de resize da página
    page.on_resize = handle_resize
    
    # Inicialização
    settings = Settings()
    solitaire = Solitaire(settings, on_win)
    solitaire.on_stats_change = update_stats
    
    # Cria a barra de topo (ajusta conforme a tua implementação de layout.py)
    create_appbar(page, settings, on_new_game, solitaire, trigger_bsod)
    
    # Adiciona o jogo já dentro do view rolável
    game_view = ft.Container(
        expand=True,
        content=ft.ListView(
            controls=[ft.Container(content=solitaire, width=SOLITAIRE_WIDTH, height=SOLITAIRE_HEIGHT)],
            expand=True,
            spacing=0,
            padding=0,
        ),
    )
    page.add(game_view)

    thread = threading.Thread(target=tick_timer, daemon=True)
    thread.start()

    solitaire.start_timer() # Começa o primeiro jogo
    handle_resize(None)
    
    # Primeira execução para ajustar ao tamanho inicial da janela
    handle_resize(None)

    # Handler de erros simples
    page.on_error = lambda e: print("Page error:", e.data)

if __name__ == "__main__":
    ft.run(main, assets_dir="assets")