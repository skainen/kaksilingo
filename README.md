# Kaksilingo

Flet application created during a hackathon day as part of a UI Programming course at Savonia University of Applied Sciences. The app's purpose is to help users learn Finnish vocabulary in English using flashcards.

To run the app:

```
flet run kaksilingo
```

To extend for specific use, you can add words to data/vocabulary.csv in form: english word,finnish word,0

You can of course use whatever languages you want.

0 is for the streak of correct answers on a word. When streak is 2, that word won't be asked again.

# Ideas for extending the app
- Using sentences instead of single words.
- Text to speech for learning pronounciation.
- Better logic for frequency of asked words. (Now it's just the streak of 2 correct answers)
