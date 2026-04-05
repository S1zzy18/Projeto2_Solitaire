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
    page.padding = 0
    page.spacing = 0

    def handle_resize(e):
        if page.width and page.height:
            # Desconto do espaço da appbar
            available_height = page.height - 40 

            scale_w = page.width / SOLITAIRE_WIDTH
            scale_h = available_height / SOLITAIRE_HEIGHT

            # Mantém a proporção e não deixa crescer além do tamanho real
            scale_factor = min(scale_w, scale_h, 1.0)
            solitaire.scale = scale_factor
            
            # Diferenciação de plataformas para não "foder" o layout
            if page.platform == ft.PagePlatform.IOS:
                # Valores que ficaram perfeitos no teu iPhone
                solitaire.offset = ft.Offset(-0.1, -0.2) 
                solitaire.alignment = ft.Alignment(-1, -1)
            else:
                # Valores padrão para Desktop/Web (centrado e sem desvio)
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
        
        page.add(solitaire)
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
    
    # Cria a barra de topo (ajusta conforme a tua implementação de layout.py)
    create_appbar(page, settings, on_new_game, solitaire)
    
    page.add(solitaire)
    
    # Primeira execução para ajustar ao tamanho inicial da janela
    handle_resize(None)

    # Handler de erros simples
    page.on_error = lambda e: print("Page error:", e.data)

if __name__ == "__main__":
    ft.run(main, assets_dir="assets")