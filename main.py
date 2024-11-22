import flet as ft
from models.flashcard import FlashcardGame
from components.card import create_card_container, create_input_controls
from utils.event_handlers import EventHandlers
import random
from math import pi

def main(page: ft.Page):
    # Set window properties
    page.window_width = 1200   # Width in pixels
    page.window_height = 800   # Height in pixels
    page.window_resizable = False  # Optional: prevent window resizing
    
    # Rest of your window settings
    page.title = "Language Learning Flashcards"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = "dark"
    page.padding = 20

    # Logo animation setup
    size = 40
    gap = 6
    duration = 2000

    c1 = ft.colors.PINK_500
    c2 = ft.colors.AMBER_500
    c3 = ft.colors.LIGHT_GREEN_500
    c4 = ft.colors.DEEP_PURPLE_500
    c5 = ft.colors.CYAN_700

    all_colors = [
        ft.colors.AMBER_400,
        ft.colors.AMBER_ACCENT_400,
        ft.colors.BLUE_400,
        ft.colors.BROWN_400,
        ft.colors.CYAN_700,
        ft.colors.DEEP_ORANGE_500,
        ft.colors.CYAN_500,
        ft.colors.INDIGO_600,
        ft.colors.ORANGE_ACCENT_100,
        ft.colors.PINK,
        ft.colors.RED_600,
        ft.colors.GREEN_400,
        ft.colors.GREEN_ACCENT_200,
        ft.colors.TEAL_ACCENT_200,
        ft.colors.LIGHT_BLUE_500,
    ]

    # Coordinates for "Kaksi" (line 1) and "Lingo" (line 2)
    parts = [
        # K (line 1)
        (0, 0, c1), (0, 1, c1), (0, 2, c1), (0, 3, c1), (0, 4, c1),
        (1, 2, c1), (2, 1, c1), (2, 3, c1), (3, 0, c1), (3, 4, c1),
        # A (line 1)
        (5, 0, c2), (6, 0, c2), (4, 1, c2), (7, 1, c2), (4, 2, c2),
        (5, 2, c2), (6, 2, c2), (7, 2, c2), (4, 3, c2), (7, 3, c2),
        (4, 4, c2), (7, 4, c2),
        # K (line 1)
        (9, 0, c3), (9, 1, c3), (9, 2, c3), (9, 3, c3), (9, 4, c3),
        (10, 2, c3), (11, 1, c3), (11, 3, c3), (12, 0, c3), (12, 4, c3),
        # S (line 1)
        (14, 0, c4), (15, 0, c4), (16, 0, c4), (14, 1, c4),
        (14, 2, c4), (15, 2, c4), (16, 2, c4), (16, 3, c4), (16, 4, c4),
        (15, 4, c4), (14, 4, c4),
        # I (line 1)
        (18, 0, c5), (19, 0, c5), (20, 0, c5), (19, 1, c5), (19, 2, c5),
        (19, 3, c5), (18, 4, c5), (19, 4, c5), (20, 4, c5),
        # L (line 2)
        (0, 6, c1), (0, 7, c1), (0, 8, c1), (0, 9, c1), (0, 10, c1),
        (1, 10, c1), (2, 10, c1),
        # I (line 2)
        (4, 6, c2), (5, 6, c2), (6, 6, c2), (5, 7, c2), (5, 8, c2),
        (5, 9, c2), (4, 10, c2), (5, 10, c2), (6, 10, c2),
        # N (line 2)
        (8, 6, c3), (8, 7, c3), (8, 8, c3), (8, 9, c3), (8, 10, c3),
        (9, 7, c3), (10, 8, c3), (11, 9, c3), (11, 6, c3), (11, 7, c3),
        (11, 10, c3),
        # G (line 2)
        (13, 7, c4), (14, 6, c4), (15, 6, c4), (13, 8, c4),
        (16, 8, c4), (16, 9, c4), (15, 10, c4), (14, 10, c4), (13, 9, c4),
        (15, 8, c4),
        # O (line 2)
        (18, 7, c5), (19, 6, c5), (20, 6, c5), (21, 7, c5), (21, 8, c5),
        (21, 9, c5), (20, 10, c5), (19, 10, c5), (18, 9, c5), (18, 8, c5),
    ]

    width = 23 * (size + gap)
    height = 12 * (size + gap)

    # Create game components (initially hidden)
    game = FlashcardGame()
    
    initial_word = game.current_word.english
    card_text = ft.Text(
        value=initial_word,
        size=30,
        text_align=ft.TextAlign.CENTER,
        weight=ft.FontWeight.BOLD,
    )

    direction_text = ft.Text(
        value="English → Finnish",
        size=16,
        color=ft.colors.GREY_700,
        text_align=ft.TextAlign.CENTER,
    )

    result_text = ft.Text(
        value="",
        size=16,
        text_align=ft.TextAlign.CENTER,
        visible=False,
    )

    guess_input, submit_btn, next_btn, switch_btn = create_input_controls()
    card_container = create_card_container(direction_text, card_text, lambda _: show_word())
    
    handlers = EventHandlers(
        game=game,
        card_container=card_container,
        card_text=card_text,
        direction_text=direction_text,
        guess_input=guess_input,
        submit_btn=submit_btn,
        next_btn=next_btn,
        result_text=result_text,
        page=page
    )

    guess_input.visible = True
    submit_btn.visible = True
    guess_input.label = "Finnish translation"

    submit_btn.on_click = handlers.check_answer
    next_btn.on_click = handlers.next_word
    switch_btn.on_click = handlers.switch_language

    # Create game content container (initially hidden)
    game_content = ft.Container(
        visible=False,
        content=ft.Column(
            [
                card_container,
                result_text,
                ft.Column(
                    [
                        guess_input,
                        submit_btn,
                        next_btn,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                ),
                switch_btn,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=30,
        ),
    )

    # Logo animation setup
    canvas = ft.Stack(
        width=width,
        height=height,
        animate_scale=duration,
        animate_opacity=duration,
    )

    for i in range(len(parts)):
        canvas.controls.append(
            ft.Container(
                animate=duration,
                animate_position=duration,
                animate_rotation=duration,
            )
        )

    def start_game(e):
        canvas.visible = False
        start_button.visible = False
        game_content.visible = True
        page.update()

    def randomize():
        random.seed()
        for i in range(len(parts)):
            c = canvas.controls[i]
            part_size = random.randrange(int(size / 2), int(size * 3))
            c.left = random.randrange(0, width)
            c.top = random.randrange(0, height)
            c.bgcolor = all_colors[random.randrange(0, len(all_colors))]
            c.width = part_size
            c.height = part_size
            c.border_radius = random.randrange(0, int(size / 2))
            c.rotate = random.randrange(0, 90) * 2 * pi / 360
        canvas.scale = 5
        canvas.opacity = 0.3
        page.update()

    def assemble():
        i = 0
        for left, top, bgcolor in parts:
            c = canvas.controls[i]
            c.left = left * (size + gap)
            c.top = top * (size + gap)
            c.bgcolor = bgcolor
            c.width = size
            c.height = size
            c.border_radius = 5
            c.rotate = 0
            i += 1
        canvas.scale = 1
        canvas.opacity = 1
        start_button.visible = True
        page.update()

    # Start button (initially hidden)
    start_button = ft.ElevatedButton(
        "Start Game",
        on_click=start_game,
        visible=False,
        style=ft.ButtonStyle(
            padding=ft.padding.all(20),
            shape=ft.RoundedRectangleBorder(radius=10),
        )
    )

    # Add everything to the page
    page.add(
        canvas,
        start_button,
        game_content
    )

    # Start the animation sequence - do randomize and assemble immediately
    randomize()
    page.update()
    assemble()

if __name__ == "__main__":
    ft.app(target=main)