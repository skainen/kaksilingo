import random

class word:
    all_words = []
    def __init__(self,name,translation,streak=0):
        self.name = name
        self.translation = translation
        self.streak = streak

        streak = 0
        word.all_words.append(self)

    def __repr__(self):
        return f'{self.name} - {self.translation}'
    
    def ask_word(self):
        local_translation = input(f'What is translation for {self.name}? ')
        if local_translation == self.translation:
            print('correct!')
            self.streak = self.streak+1
        else:
            print('incorrect!')
            self.strea=self.streak-1
    
    @classmethod
    def print_random(cls):
        ls = word.all_words
        print(ls)
        



w1 = word('yksi','one')
w2 = word('kahvi','coffee')
w3 = word('pussi','bag')
w4 = word('koira','dog')
w5 = word('olut','beer')

"""
while True:
    xword = random.choice(word.all_words)
    if xword.streak <= 2:
        xword.ask_word()
        print(xword.streak)
    elif xword.streak >=3 :
        coef = random.randint(0,xword.streak)
        if coef <=1:
            xword.ask_word()
"""
word.print_random()    
