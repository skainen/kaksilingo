import random
import csv
from datetime import datetime
from pathlib import Path

class FlashcardGame:
    def __init__(self):
        self.words = [
            {"english": "Hello", "finnish": ["Hei", "Moi", "Terve", "Moikka", "Tervehdys"]},
            {"english": "Goodbye", "finnish": ["Näkemiin", "Heippa", "Moi moi", "Hyvästi"]},
            {"english": "Thank you", "finnish": ["Kiitos", "Kiitti"]},
            {"english": "Please", "finnish": ["Ole hyvä", "Olkaa hyvä"]},
            {"english": "Good morning", "finnish": ["Hyvää huomenta", "Huomenta"]},
            {"english": "Yes", "finnish": ["Kyllä", "Joo", "Juu"]},
            {"english": "No", "finnish": ["Ei", "Eipä"]},
            {"english": "How are you?", "finnish": ["Mitä kuuluu?", "Miten menee?"]},
            {"english": "Good evening", "finnish": ["Hyvää iltaa", "Iltaa"]},
            {"english": "Welcome", "finnish": ["Tervetuloa"]}
        ]
        self.current_word = random.choice(self.words)
        self.is_flipped = False
        self.finnish_to_english = False
        self.history_file = "flashcard_history.csv"
        self._init_history_file()

    def _init_history_file(self):
        if not Path(self.history_file).exists():
            with open(self.history_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Timestamp', 'Question Language', 'Asked Word', 'Correct Translations', 'User Answer', 'Correct'])

    def log_attempt(self, user_answer, correct):
        with open(self.history_file, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            asked_word = self.current_word["finnish"][0] if self.finnish_to_english else self.current_word["english"]
            correct_answers = self.current_word["english"] if self.finnish_to_english else ", ".join(self.current_word["finnish"])
            question_language = "Finnish" if self.finnish_to_english else "English"
            
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                question_language,
                asked_word,
                correct_answers,
                user_answer,
                correct
            ])