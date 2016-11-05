from utils.utils import mark_up_as_string
from utils.utils import write_to_csv
from utils.parsers import parse_gallons, parse_date, parse_location
from bs4 import BeautifulSoup


def generate_csv():
    """ Relevent mark up was taken from
    https://en.wikipedia.org/wiki/List_of_pipeline_accidents_in_the_United_States_in_the_21st_century
    starting with first <h3> tag
    """
    markup_string = mark_up_as_string('wiki_markup.html')
    soup = BeautifulSoup(markup_string, 'html.parser')
    content = soup.contents
    header = [
        'city',
        'state',
        'ref_link',
        'gallons',
        'description',
        'date',
        'latitude',
        'longitude',
        'accident_type'
    ]
    data = []
    for ch in content:
        if ch.name == 'h3':
            year = ch.text[:4]
        if ch.name == 'ul':
            ul = ch
            for li in ul.contents:
                description = li.text
                gallons = parse_gallons(description)
                city, state, lat, lng = parse_location(description)
                date = parse_date(description, year)
                ref_link = 'N/A' # TODO: make get_ref parser
                accident_type = 'oil'
                if 'natural gas' in description.lower():
                    accident_type = 'gas'

                row = [
                    city,
                    state,
                    ref_link,
                    gallons,
                    description,
                    date,
                    lat,
                    lng,
                    accident_type
                ]
                data.append(row)

    write_to_csv(data, header, 'pipe-data.csv')


generate_csv()
