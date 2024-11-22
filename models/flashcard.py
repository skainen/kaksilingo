import random
import csv
from datetime import datetime
from pathlib import Path
from collections import defaultdict

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
        # Only show if streak is less than 2
        return self.streak < 2

class FlashcardGame:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.resolve()
        self._ensure_data_structure()
        self.streaks = self._load_streaks()  # Load streaks before loading words
        self.words = self._load_words_from_csv()
        if not self.words:
            print("Error: vocabulary.csv is empty. Please add words in the format:")
            raise FileNotFoundError("vocabulary.csv is empty. Please add some words.")
            
        self.current_word = self._select_next_word()
        self.is_flipped = False
        self.finnish_to_english = False
        self.history_file = self.base_path / "history" / "flashcard_history.csv"
        self._init_history_file()

    def _load_streaks(self):
        """Load the latest streak for each word from history file."""
        streaks = defaultdict(int)
        history_file = self.base_path / "history" / "flashcard_history.csv"
        
        if history_file.exists():
            with open(history_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    word = row['Asked Word']
                    streak = int(row['Streak'])
                    streaks[word] = streak  # This will keep updating, so we'll end up with the latest streak
        
        return streaks

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
        vocab_file = self.base_path / 'data' / 'vocabulary.csv'
        try:
            with open(vocab_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Look up streak from history
                    streak = self.streaks.get(row['english'], 0)  # Get English word streak
                    finnish_streak = self.streaks.get(row['finnish'].split(';')[0], 0)  # Get Finnish word streak
                    # Use the maximum streak found
                    max_streak = max(streak, finnish_streak)
                    
                    words.append(Word(
                        english=row['english'],
                        finnish_translations=row['finnish'],
                        streak=max_streak
                    ))
        except Exception as e:
            print(f"Error reading vocabulary file: {e}")
            print(f"Expected file location: {vocab_file}")
            raise
        return words

    def get_current_word_dict(self):
        return self.current_word.to_dict()

    def _select_next_word(self):
        # Only select words with streak < 2
        eligible_words = [word for word in self.words if word.streak < 2]
        
        # If no eligible words (all have high streaks), reset all streaks
        if not eligible_words:
            print("All words have been learned! Resetting streaks...")
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