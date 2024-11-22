import random
import csv
from datetime import datetime
from pathlib import Path

class Word:
    def __init__(self, english, finnish_translations, streak=0):
        self.english = english
        self.finnish_translations = finnish_translations
        self.streak = streak

    def to_dict(self):
        return {
            "english": self.english,
            "finnish": self.finnish_translations
        }

    def should_show(self):
        if self.streak <= 2:
            return True
        return random.randint(0, self.streak) <= 1

class FlashcardGame:
    def __init__(self):
        self.words = [
            Word("Hello", ["Hei", "Moi", "Terve", "Moikka", "Tervehdys"]),
            Word("Goodbye", ["Näkemiin", "Heippa", "Moi moi", "Hyvästi"]),
            Word("Thank you", ["Kiitos", "Kiitti"]),
            Word("Please", ["Ole hyvä", "Olkaa hyvä"]),
            Word("Good morning", ["Hyvää huomenta", "Huomenta"]),
            Word("Yes", ["Kyllä", "Joo", "Juu"]),
            Word("No", ["Ei", "Eipä"]),
            Word("How are you?", ["Mitä kuuluu?", "Miten menee?"]),
            Word("Good evening", ["Hyvää iltaa", "Iltaa"]),
            Word("Welcome", ["Tervetuloa"])
        ]
        self.current_word = self._select_next_word()
        self.is_flipped = False
        self.finnish_to_english = False
        self.history_file = "flashcard_history.csv"
        self._init_history_file()

    def get_current_word_dict(self):
        return self.current_word.to_dict()

    def _select_next_word(self):
        eligible_words = [word for word in self.words if word.should_show()]
        if not eligible_words:
            for word in self.words:
                word.streak = 0
            eligible_words = self.words
        return random.choice(eligible_words)

    def update_streak(self, correct):
        if correct:
            self.current_word.streak += 1
        else:
            self.current_word.streak = max(0, self.current_word.streak - 1)

    def _init_history_file(self):
        if not Path(self.history_file).exists():
            with open(self.history_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([
                    'Timestamp', 
                    'Question Language', 
                    'Asked Word', 
                    'Correct Translations', 
                    'User Answer', 
                    'Correct',
                    'Streak'
                ])

    def log_attempt(self, user_answer, correct):
        self.update_streak(correct)
        
        with open(self.history_file, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            word_dict = self.get_current_word_dict()
            asked_word = word_dict["finnish"][0] if self.finnish_to_english else word_dict["english"]
            correct_answers = word_dict["english"] if self.finnish_to_english else ", ".join(word_dict["finnish"])
            question_language = "Finnish" if self.finnish_to_english else "English"
            
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                question_language,
                asked_word,
                correct_answers,
                user_answer,
                correct,
                self.current_word.streak
            ])