import flet as ft
import random
from models.flashcard import FlashcardApp
from components.card_display import CardDisplay
from components.add_card_dialog import AddCardDialog

def main(page: ft.Page):
    app = FlashcardApp()
    
    # Page setup
    page.title = "Language Learning Flashcards"
    page.theme_mode = "light"
    page.window_width = 600
    page.window_height = 400
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Card text control
    card_text = ft.Text(
        value=app.cards[0]["front"],
        size=30,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER
    )

    def flip_card(e):
        app.card_flipped = not app.card_flipped
        current_card = app.get_current_card()
        card_text.value = current_card["back"] if app.card_flipped else current_card["front"]
        page.update()

    def next_card(e):
        card_text.value = app.next_card()
        page.update()

    def previous_card(e):
        card_text.value = app.previous_card()
        page.update()

    def shuffle_cards(e):
        random.shuffle(app.cards)
        app.current_card_index = 0
        app.card_flipped = False
        card_text.value = app.cards[0]["front"]
        page.update()

    def save_new_card(front, back, language):
        app.add_card(front, back, language)

    # Initialize components
    card_display = CardDisplay(app.cards[0]["front"], flip_card)
    add_dialog = AddCardDialog(save_new_card)

    def open_add_dialog(e):
        page.dialog = add_dialog.build()
        page.dialog.open = True
        page.update()

    # Main layout
    page.add(
        ft.Column(
            [
                card_display,
                ft.Row(
                    [
                        ft.ElevatedButton("Previous", on_click=previous_card),
                        ft.ElevatedButton("Flip", on_click=flip_card),
                        ft.ElevatedButton("Next", on_click=next_card),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        ft.ElevatedButton("Shuffle", on_click=shuffle_cards),
                        ft.ElevatedButton("Add Card", on_click=open_add_dialog),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

if __name__ == "__main__":
    ft.app(target=main)