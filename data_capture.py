from states import states_dict
from months import months_list
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
import string


def mark_up_as_string(f):
    with open(f, 'r') as mu:
        markup = mu.read().replace('\n', '')
    return markup

def read_wiki_data():
    markup_string = mark_up_as_string('wiki_markup.html')
    soup = BeautifulSoup(markup_string, 'html.parser')
    content = soup.contents
    data = []
    for ch in content:
        if ch.name == 'h3':
            year = ch.text[:4]
        if ch.name == 'ul':
            ul = ch
            for li in ul.contents:
                description = li.text
                if 'natural gas' in description.lower():
                    accident_type = 'gas'
                else:
                    accident_type = 'oil'
                print extract_gallons(description)
                # for child in li.children: # need to get ref links
                #     print child
                # city, state, lat, lng = extract_location(description)
                # print description
                # print city
                # print state
                # print lat
                # print lng

def strip_punc(s):
    clean_string = s
    for ch in string.punctuation:
        clean_string = clean_string.strip(ch)
    return clean_string

def parse_gallons(description):
    """ returns number before string 'gallons' within description """
    num_gallons = 'N/A'
    description_list = [strip_punc(s) for s in description.split()]
    for word in description_list:
        w = word.lower()
        if w == 'gallons':
            num_gallons_index = description_list.index(word) - 1
            num_gallons = description_list[num_gallons_index]
            num_gallons = num_gallons.replace(',','')
            try:
                int(num_gallons)
            except ValueError, TypeError:
                num_gallons = 'N/A'
    return num_gallons


def parse_date(description, year):
    """Return string in YEAR-MONTH-DATE format.
       Contingent on month being followed by an int
       eg. March 5"""
    description_list = [strip_punc(s) for s in description.split()]
    for month in months_list: # Assume month is properly captialized
        if month in description_list:
            month_num = months_list.index(month) + 1  # Compensate for zero index
            month_num = str(month_num).zfill(2)
            day = description_list[description_list.index(month) + 1]
            day = day.zfill(2)
            try:
                int(day)
            except ValueError: # The month was not followed by an integer
                day = '01'
            return year + '-' + str(month_num) + '-' + str(day)


def parse_location(description):
    """ contingent on city preceding state, e.g Austin, Texas
    NOTE: returns first occurence of this pattern within description"""
    geolocator = Nominatim()
    description_list = [strip_punc(s) for s in description.split()]
    for state in states_dict.values():  # Assume state is properly capitalized
        if state in description_list:
            city = description_list[description_list.index(state) - 1]
            location = geolocator.geocode(city + ', ' + state)
            try:
                lat = location.latitude
                lng = location.longitude
            except AttributeError:  # The preceding item was not a city
                city = 'N/A'
                location = geolocator.geocode(state)
                lat = location.latitude
                lng = location.longitude
            return city, state, lat, lng

read_wiki_data()
