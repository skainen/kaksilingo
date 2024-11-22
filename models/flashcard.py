import random
import csv
from datetime import datetime
from pathlib import Path

class FlashcardGame:
    def __init__(self):
        self.words = [
            {"word": "Hello", "translation": "Hei"},
            {"word": "Goodbye", "translation": "Näkemiin"},
            {"word": "Thank you", "translation": "Kiitos"},
            {"word": "Please", "translation": "Ole hyvä"},
            {"word": "Good morning", "translation": "Hyvää huomenta"},
            {"word": "Yes", "translation": "Kyllä"},
            {"word": "No", "translation": "Ei"},
            {"word": "How are you?", "translation": "Mitä kuuluu?"},
            {"word": "Good evening", "translation": "Hyvää iltaa"},
            {"word": "Welcome", "translation": "Tervetuloa"}
        ]
        self.current_word = random.choice(self.words)
        self.is_flipped = False
        self.history_file = "flashcard_history.csv"
        self._init_history_file()

    def _init_history_file(self):
        if not Path(self.history_file).exists():
            with open(self.history_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Timestamp', 'English', 'Finnish', 'User Answer', 'Correct'])

    def log_attempt(self, user_answer, correct):
        with open(self.history_file, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                self.current_word["word"],
                self.current_word["translation"],
                user_answer,
                correct
            ])