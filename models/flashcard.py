import json
from pathlib import Path

class FlashcardApp:
    def __init__(self):
        self.current_card_index = 0
        self.cards = []
        self.card_flipped = False
        self.load_cards()

    def load_cards(self):
        if not Path("flashcards.json").exists():
            self.cards = [
                {"front": "Hello", "back": "Hola", "language": "Spanish"},
                {"front": "Goodbye", "back": "Adiós", "language": "Spanish"},
                {"front": "Thank you", "back": "Gracias", "language": "Spanish"}
            ]
            self.save_cards()
        else:
            with open("flashcards.json", "r", encoding="utf-8") as f:
                self.cards = json.load(f)

    def save_cards(self):
        with open("flashcards.json", "w", encoding="utf-8") as f:
            json.dump(self.cards, f, ensure_ascii=False, indent=2)

    def add_card(self, front: str, back: str, language: str):
        new_card = {"front": front, "back": back, "language": language}
        self.cards.append(new_card)
        self.save_cards()

    def get_current_card(self):
        return self.cards[self.current_card_index]

    def next_card(self):
        self.card_flipped = False
        self.current_card_index = (self.current_card_index + 1) % len(self.cards)
        return self.get_current_card()["front"]

    def previous_card(self):
        self.card_flipped = False
        self.current_card_index = (self.current_card_index - 1) % len(self.cards)
        return self.get_current_card()["front"]