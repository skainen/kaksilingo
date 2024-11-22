import flet as ft
import random

class EventHandlers:
    def __init__(self, game, card_container, card_text, guess_input, submit_btn, next_btn, result_text, page):
        self.game = game
        self.card_container = card_container
        self.card_text = card_text
        self.guess_input = guess_input
        self.submit_btn = submit_btn
        self.next_btn = next_btn
        self.result_text = result_text
        self.page = page

    def show_word(self, e=None):
        if not self.game.is_flipped:
            self.game.is_flipped = True
            self.card_container.scale = ft.transform.Scale(0, 1, alignment=ft.alignment.center)
            self.page.update()
            
            self.card_text.value = self.game.current_word["word"]
            self.guess_input.visible = True
            self.submit_btn.visible = True
            self.result_text.visible = False
            self.guess_input.value = ""
            self.card_container.scale = ft.transform.Scale(1, alignment=ft.alignment.center)
            self.page.update()

    def check_answer(self, e):
        user_guess = self.guess_input.value.strip().lower()
        correct_answer = self.game.current_word["translation"].lower()
        
        self.card_container.scale = ft.transform.Scale(0, 1, alignment=ft.alignment.center)
        self.page.update()
        
        self.card_text.value = self.game.current_word["translation"]
        is_correct = user_guess == correct_answer
        
        self.game.log_attempt(user_guess, is_correct)
        
        if is_correct:
            self.card_container.bgcolor = ft.colors.GREEN_200
            self.result_text.value = "Correct! 🎉"
            self.result_text.color = ft.colors.GREEN_700
        else:
            self.card_container.bgcolor = ft.colors.RED_200
            self.result_text.value = f"Not quite. The correct answer is: {self.game.current_word['translation']}"
            self.result_text.color = ft.colors.RED_700
            
        self.guess_input.visible = False
        self.submit_btn.visible = False
        self.next_btn.visible = True
        self.result_text.visible = True
        
        self.card_container.scale = ft.transform.Scale(1, alignment=ft.alignment.center)
        self.page.update()

    def next_word(self, e):
        self.game.current_word = self.game.words[random.randint(0, len(self.game.words) - 1)]
        self.game.is_flipped = False
        
        self.card_container.scale = ft.transform.Scale(0, 1, alignment=ft.alignment.center)
        self.page.update()
        
        self.card_container.bgcolor = ft.colors.WHITE
        self.card_text.value = "Click to start"
        self.next_btn.visible = False
        self.result_text.visible = False
        
        self.card_container.scale = ft.transform.Scale(1, alignment=ft.alignment.center)
        self.page.update()