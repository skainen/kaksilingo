import flet as ft
from models.flashcard import FlashcardGame
from components.card import create_card_container, create_input_controls
from utils.event_handlers import EventHandlers

def main(page: ft.Page):
    page.title = "English-Finnish Flashcards"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = "light"
    
    page.window_center()
    #page.window.set_window_size(500, 600)

    game = FlashcardGame()

    # Create UI components
    card_text = ft.Text(
        value="Click to start",
        size=30,
        text_align=ft.TextAlign.CENTER,
        weight=ft.FontWeight.BOLD,
    )

    card_subtitle = ft.Text(
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

    # Create card container and input controls
    card_container = create_card_container(card_subtitle, card_text)
    guess_input, submit_btn, next_btn = create_input_controls()

    # Initialize event handlers
    handlers = EventHandlers(
        game, card_container, card_text, guess_input,
        submit_btn, next_btn, result_text, page
    )

    # Connect event handlers
    card_container.on_click = handlers.show_word
    submit_btn.on_click = handlers.check_answer
    next_btn.on_click = handlers.next_word

    # Add everything to the page
    page.add(
        ft.Column(
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
        )
    )

if __name__ == "__main__":
    ft.app(target=main)