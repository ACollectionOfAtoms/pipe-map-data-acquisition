import string
import csv
""" TODO: add function to remove citations at end of descriptions
    regex is somthing like: \[[\d]*\] """

def strip_punc(s):
    clean_string = s
    for ch in string.punctuation:
        clean_string = clean_string.strip(ch)
    return clean_string

def mark_up_as_string(f):
    with open(f, 'r') as mu:
        markup = mu.read().replace('\n', '')
    return markup

def write_to_csv(data, header, f):
    with open(f, 'w') as fp:
        writer = csv.writer(fp, delimiter=',')
        writer.writerow(header)
        writer.writerows(data)
