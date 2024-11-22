import flet as ft
import random
from components.card import create_card_content

class EventHandlers:
    def __init__(self, game, card_container, card_text, direction_text, 
                 guess_input, submit_btn, next_btn, result_text, page):
        self.game = game
        self.card_container = card_container
        self.card_text = card_text
        self.direction_text = direction_text
        self.guess_input = guess_input
        self.submit_btn = submit_btn
        self.next_btn = next_btn
        self.result_text = result_text
        self.page = page

    def update_direction_text(self):
        return "Finnish → English" if self.game.finnish_to_english else "English → Finnish"

    def switch_language(self, e):
        self.game.finnish_to_english = not self.game.finnish_to_english
        self.direction_text.value = self.update_direction_text()
        self.next_word(None)  # Show new word directly
        self.page.update()

    def show_word(self, e=None):
        # Now just displays input controls since word is already shown
        self.guess_input.visible = True
        self.submit_btn.visible = True
        self.result_text.visible = False
        self.guess_input.value = ""
        self.page.update()

    def check_answer(self, e):
        user_guess = self.guess_input.value.strip().lower()
        
        if self.game.finnish_to_english:
            correct = user_guess.lower() == self.game.current_word["english"].lower()
            correct_answers = [self.game.current_word["english"]]
        else:
            correct = user_guess.lower() in [ans.lower() for ans in self.game.current_word["finnish"]]
            correct_answers = self.game.current_word["finnish"]
        
        self.card_text.value = "\n".join(correct_answers)
        self.game.log_attempt(user_guess, correct)
        
        new_content = create_card_content(
            self.direction_text,
            self.card_text,
            False,
            None  # Remove click handler during answer display
        )
        
        if correct:
            new_content.bgcolor = ft.colors.GREEN_200
            self.result_text.value = "Correct! 🎉"
            self.result_text.color = ft.colors.GREEN_700
        else:
            new_content.bgcolor = ft.colors.RED_200
            self.result_text.value = f"Not quite. Valid answers:\n{', '.join(correct_answers)}"
            self.result_text.color = ft.colors.RED_700
        
        self.card_container.content = new_content
        self.guess_input.visible = False
        self.submit_btn.visible = False
        self.next_btn.visible = True
        self.result_text.visible = True
        self.page.update()

    def next_word(self, e):
        self.game.current_word = random.choice(self.game.words)
        
        # Show new word directly
        if self.game.finnish_to_english:
            self.card_text.value = self.game.current_word["finnish"][0]
            self.guess_input.label = "English translation"
        else:
            self.card_text.value = self.game.current_word["english"]
            self.guess_input.label = "Finnish translation"
        
        new_content = create_card_content(
            self.direction_text,
            self.card_text,
            True,
            self.show_word
        )
        new_content.bgcolor = ft.colors.WHITE
        self.card_container.content = new_content
        
        self.next_btn.visible = False
        self.result_text.visible = False
        self.guess_input.visible = True
        self.submit_btn.visible = True
        self.page.update()