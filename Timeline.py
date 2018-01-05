#!/usr/bin/env python3

# Script written by Johanna de Vos
# January 2018

# Import modules
import os
import re
from nltk.tokenize import sent_tokenize
from texttable import Texttable

# Set working directory
os.chdir('C:/Users/johan/Dropbox/PhD/Blogs/Extracting a timeline')

# Open file
def open_file():
    with open ('Angela Merkel.txt', encoding = 'utf-8') as file:
        raw_text = file.read()
        return raw_text
    
# Preprocess the text
def preprocess_text(text):
    text = text.replace(chr(0x00AD), "") # Remove soft hyphens
    text = text.replace("\n\n", "\n") # Remove spurious white lines
    return text

# Split text into sentences
def sent_splitter(text):
    sents = sent_tokenize(text)
    
    # Manually separate headings, because sent_tokenize does not split after '\n'
    sents2 = [i.split("\n") for i in sents]
    sents = [item for sublist in sents2 for item in sublist]
    
    return sents

# Extract dates from text with a regular expression
def extract_dates(sents):
    bio = []
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    
    for sent in sents:
        matches = re.finditer(r"(?:(?P<dayPre>\d{1,2})(?:th|st|nd|rd)?(?: of)? )?"
                               "(?P<month>January|February|March|April|May|June"
                               "|July|August|September|October|November|December)?"
                               "(?: (?P<dayPost>\d{1,2})(?:th|st|nd|rd)?,)? ?"
                               "(?P<year>\d{4})", sent)
        
        # Extract year, month and day from matches
        for match in matches:
            #print(match.groups())
            year = match.group('year')
            date = year
            
            # Months are optional
            if match.group('month'):
                month = match.group('month')
                month = str(months.index(month)+1) # Express month as a digit (makes it easier to sort months)
                date += "-" + month
                
            # Days are also optional
            if match.group('dayPre'):
                day = match.group('dayPre')
                date += "-" + day
            elif match.group('dayPost'):
                day = match.group('dayPost')
                date += "-" + day
            
            # Append the (date, sent) tuple to the biography list
            bio.append((date, sent))
            
    return bio

# Sort dates chronologically    
def sort_dates(bio):
    bio.sort(key=lambda x: x[0])
    return bio

# Start the timeline with the year the person was born
def after_birth(bio_sorted):
    while True:
    
        for i in range(len(bio_sorted)):                       

            if "born" in bio_sorted[i][1]:            
                index = i
                break
            
        break
    
    bio_from_birth = bio_sorted[index:]
    return bio_from_birth

# Make and print table
def make_table(bio_sorted):
    bio_table = Texttable()
    for date, sent in bio_sorted:
        bio_table.add_row([date, sent])
    print(bio_table.draw())
    return bio_table

# Run code
if __name__ == "__main__":
    raw_text = open_file()
    prep_text = preprocess_text(raw_text)
    sents = sent_splitter(prep_text)
    bio = extract_dates(sents)
    bio_sorted = sort_dates(bio)
    bio_from_birth = after_birth(bio_sorted)
    bio_table = make_table(bio_from_birth)