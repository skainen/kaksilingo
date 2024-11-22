import csv 
from wordrootclass import word


with open('default_words.csv','r') as csvfile:
    csv_reader = csv.reader(csvfile)

    for row in csv_reader:
        w1=word(row[0],row[1],row[2])

print(word.all_words)        