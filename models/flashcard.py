import random
import csv
from datetime import datetime
from pathlib import Path

class Word:
    def __init__(self, english, finnish_translations, streak=0):
        self.english = english
        self.finnish_translations = finnish_translations.split(';') if isinstance(finnish_translations, str) else finnish_translations
        self.streak = streak

    def to_dict(self):
        return {
            "english": self.english,
            "finnish": self.finnish_translations
        }

    def should_show(self):
        # If streak is 2 or less, always show
        if self.streak <= 2:
            return True
        # If streak > 2, show with decreasing probability
        coef = random.randint(0, self.streak)
        return coef <= 1

class FlashcardGame:
    def __init__(self):
        self.base_path = Path('/home/webman/fp/kaksilingo')
        self._ensure_data_structure()
        self.words = self._load_words_from_csv()
        if not self.words:
            print("Error: vocabulary.csv is empty. Please add words in the format:")
            raise FileNotFoundError("vocabulary.csv is empty. Please add some words.")
            
        self.current_word = self._select_next_word()
        self.is_flipped = False
        self.finnish_to_english = False
        self.history_file = self.base_path / "history/flashcard_history.csv"
        self._init_history_file()

    def _ensure_data_structure(self):
        data_dir = self.base_path / 'data'
        data_dir.mkdir(parents=True, exist_ok=True)
        
        vocab_file = data_dir / 'vocabulary.csv'
        if not vocab_file.exists():
            with open(vocab_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['english', 'finnish'])

    def _load_words_from_csv(self):
        words = []
        vocab_file = self.base_path / 'data/vocabulary.csv'
        with open(vocab_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                words.append(Word(
                    english=row['english'],
                    finnish_translations=row['finnish']
                ))
        return words

    def get_current_word_dict(self):
        return self.current_word.to_dict()

    def _select_next_word(self):
        # Filter words based on streak probability
        eligible_words = [word for word in self.words if word.should_show()]
        
        # If no eligible words (all have high streaks), reset all streaks
        if not eligible_words:
            for word in self.words:
                word.streak = 0
            eligible_words = self.words
            
        return random.choice(eligible_words)

    def update_streak(self, correct):
        if correct:
            self.current_word.streak += 1
        else:
            # Decrease streak by 1, but don't go below 0
            self.current_word.streak = max(0, self.current_word.streak - 1)

    def _init_history_file(self):
        history_dir = self.base_path / 'history'
        history_dir.mkdir(parents=True, exist_ok=True)
        
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