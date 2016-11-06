from utils.utils import mark_up_as_string
from utils.utils import write_to_csv
from utils.parsers import parse_gallons, parse_date, parse_location
from bs4 import BeautifulSoup
import progressbar


def generate_csv():
    """ Relevent mark up was taken from
    https://en.wikipedia.org/wiki/List_of_pipeline_accidents_in_the_United_States_in_the_21st_century
    starting with first <h3> tag

    TODO: Implement ability to write directly to disk so the script can pick up where it left off
    incase of connection issues with geopy providers or otherwise.
    TODO: Implement ability to re-run script and update csv with new markup data rather than re-parsing
    entire document.
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
    skipped = 0

    for ch in content:
        if ch.name == 'h3':
            year = ch.text[:4]
        if ch.name == 'ul':
            ul = ch
            progress_i = 0
            bar = progressbar.ProgressBar(maxval=len(ul.contents), \
                                          widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
            bar.start()

            for li in ul.contents:
                progress_i += 1
                bar.update(progress_i)
                description = li.text
                gallons = parse_gallons(description)
                location_results = parse_location(description)
                if location_results is None:
                    skipped += 1
                    continue  # We failed to get location data!
                city, state, lat, lng = location_results
                date = parse_date(description, year)
                if date is None:
                    skipped += 1
                    continue  # No date? :(
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
                row = [s.encode('utf-8') for s in row]
                data.append(row)
                bar.finish()
    write_to_csv(data, header, 'pipe-data.csv')
    print 'Data written to CSV. Descriptions skipped: ' + str(skipped)


generate_csv()
