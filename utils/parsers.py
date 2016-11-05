from geopy.geocoders import Nominatim
from utils import strip_punc
from refs.states import states_dict
from refs.months import months_list
""" TODO: Add method to parse citations, barrels """


def parse_gallons(description):
    """ returns number before the 'gallons' substring within description """
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
       e.g. March 5"""
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
