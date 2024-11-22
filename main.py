import flet as ft
from models.flashcard import FlashcardGame
from components.card import create_card_container, create_input_controls
from utils.event_handlers import EventHandlers

def main(page: ft.Page):
    page.title = "Language Learning Flashcards"
    page.vertical_alignment = ft.MainAxisAlignment.START  # Changed to START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = "dark"
    
    page.window.width = 500
    page.window.height = 700
    page.padding = 20

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

    # Create top content container
    top_content = ft.Container(
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
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=30,
        ),
        alignment=ft.alignment.top_center,
        margin=ft.margin.only(top=40),  # Add some top margin
    )

    # Create bottom container for switch button
    bottom_content = ft.Container(
        content=switch_btn,
        alignment=ft.alignment.center,
        expand=True,  # This will push the container to take remaining space
    )

    # Main column containing both containers
    main_column = ft.Column(
        [
            top_content,
            bottom_content
        ],
        expand=True,  # This makes the column fill the available space
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,  # This spreads out the containers
    )

    page.add(main_column)

if __name__ == "__main__":
    ft.app(target=main)