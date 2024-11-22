import flet as ft
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
        # Clear input before switching
        self.guess_input.value = ""
        self.next_word(None)
        self.page.update()

    def show_word(self, e=None):
        self.guess_input.visible = True
        self.submit_btn.visible = True
        self.result_text.visible = False
        self.guess_input.value = ""
        self.page.update()

    def check_answer(self, e):
        user_guess = self.guess_input.value.strip().lower()
        current_word_dict = self.game.get_current_word_dict()
        
        if self.game.finnish_to_english:
            correct = user_guess.lower() == current_word_dict["english"].lower()
            correct_answers = [current_word_dict["english"]]
            display_answer = current_word_dict["english"]
        else:
            correct = user_guess.lower() in [ans.lower() for ans in current_word_dict["finnish"]]
            correct_answers = current_word_dict["finnish"]
            display_answer = ", ".join(correct_answers)
        
        self.card_text.value = display_answer
        self.game.log_attempt(user_guess, correct)
        
        new_content = create_card_content(
            self.direction_text,
            self.card_text,
            False,
            None
        )
        
        if correct:
            new_content.bgcolor = ft.colors.GREEN_200
            streak_info = f" (Streak: {self.game.current_word.streak})" if self.game.current_word.streak > 1 else ""
            self.result_text.value = f"Correct! 🎉{streak_info}"
            self.result_text.color = ft.colors.GREEN_700
        else:
            new_content.bgcolor = ft.colors.RED_200
            self.result_text.value = f"Not quite. Valid answer{'s' if len(correct_answers) > 1 else ''}: {display_answer}"
            self.result_text.color = ft.colors.RED_700
        
        self.card_container.content = new_content
        self.guess_input.visible = False
        self.submit_btn.visible = False
        self.next_btn.visible = True
        self.result_text.visible = True
        self.page.update()

    def next_word(self, e):
        # Clear input first thing and force an update
        self.guess_input.value = ""
        self.page.update()
        
        self.game.current_word = self.game._select_next_word()
        current_word_dict = self.game.get_current_word_dict()
        
        if self.game.finnish_to_english:
            # When Finnish is shown, only show the first Finnish translation
            self.card_text.value = current_word_dict["finnish"][0]
            self.guess_input.label = "English translation"
        else:
            self.card_text.value = current_word_dict["english"]
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
        
        # Force another update at the end
        self.page.update()