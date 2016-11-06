import string
import csv
import re


def remove_citations(s):
    cleaner_string = re.sub('\[[\d]*\]', '', s)
    return cleaner_string

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
