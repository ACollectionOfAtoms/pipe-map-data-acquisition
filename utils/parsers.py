from geopy.geocoders import Nominatim
from geopy.exc import GeocoderServiceError
from utils import strip_punc, remove_citations
from refs.states import states_dict
from refs.months import months_list
import time

""" TODO: Add method to parse citations, number of barrels """


def parse_gallons(description):
    """ returns number before the 'gallons' substring within description """
    num_gallons = 'N/A'
    description = remove_citations(description)
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
    description = remove_citations(description)
    description_list = [strip_punc(s) for s in description.split()]
    # TODO: month_list is sorted, this can be optimized.
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

def init_geolocator(attempt=0, max_retries=8):
    """ Recursively attempt geolocator intialization """
    if attempt < max_retries:
        try:
            geolocator = Nominatim(timeout=20)
            return geolocator
        except GeocoderServiceError:
            time.sleep(2)
            attempt += 1
            init_geolocator(attempt)
    else:
        return None  # we tried :(



def parse_location(description):
    """
    Contingent on city preceding state, e.g Austin, Texas
    NOTE: returns first occurence of this pattern within description
    TODO: this function along with the above should be it's own class
    which implements retry logic and cycles through geo services if needed
    TODO: Handle case where city is more than one word;
          Handle case where no state name substring exists! (only city provided)"""
    geolocator = init_geolocator()
    if geolocator == None:
        return None
    description = remove_citations(description)
    description_list = [strip_punc(s) for s in description.split()]
    print description_list
    for state in states_dict.values():  # Assume state is properly capitalized
        if state in description:
            try:
                state_name_length = len(state.split()) # 'North Carolina' is length 2
                state_name_marker = state.split()[-1] # Get 'Carolina' substring
                state_list_location = description_list.index(state_name_marker)
                city = description_list[state_list_location - state_name_length]
                location = geolocator.geocode(city + ', ' + state)
                lat = str(location.latitude)
                lng = str(location.longitude)
            # The preceding item in the list was not a city
            # or the state found in the description was partial
            # e.g 'Alaskan'
            except (AttributeError, ValueError):
                city = 'N/A'
                location = geolocator.geocode(state)
                lat = str(location.latitude)
                lng = str(location.longitude)
            return city, state, lat, lng
