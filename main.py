import flet as ft
from models.flashcard import FlashcardGame
from components.card import create_card_container, create_input_controls
from utils.event_handlers import EventHandlers

def main(page: ft.Page):
    page.title = "Language Learning Flashcards"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = "dark"
    
    page.window_center()

    game = FlashcardGame()

    # Create UI components with initial word
    initial_word = game.current_word["english"]
    card_text = ft.Text(
        value=initial_word,  # Show first word immediately
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

    # Initialize handlers
    handlers = EventHandlers(
        game=game,
        card_container=None,
        card_text=card_text,
        direction_text=direction_text,
        guess_input=None,
        submit_btn=None,
        next_btn=None,
        result_text=result_text,
        page=page
    )

    # Create card container and input controls
    card_container = create_card_container(direction_text, card_text, handlers.show_word)
    guess_input, submit_btn, next_btn, switch_btn = create_input_controls()

    # Make input controls initially visible since we're showing word directly
    guess_input.visible = True
    submit_btn.visible = True
    guess_input.label = "Finnish translation"  # Set initial label

    # Update handlers with created components
    handlers.card_container = card_container
    handlers.guess_input = guess_input
    handlers.submit_btn = submit_btn
    handlers.next_btn = next_btn

    # Connect event handlers
    submit_btn.on_click = handlers.check_answer
    next_btn.on_click = handlers.next_word
    switch_btn.on_click = handlers.switch_language

    # Add everything to the page
    page.add(
        ft.Column(
            [
                switch_btn,
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