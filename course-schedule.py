import sys
import uuid
from icalendar import Calendar, Event
from datetime import datetime, timedelta, time
# from pytz import UTC # timezone
from bs4 import BeautifulSoup

cal = Calendar()
cal.add('prodid', '-//CPT-schedule-parser//mxm.dk//')
cal.add('version', '1.0')

soup = BeautifulSoup(open(sys.argv[1], 'r').read(), 'html.parser')

def add_event(start, end, content):
    event = Event()
    event.add('summary', content)
    event.add('dtstart', start)
    event.add('dtend', end)
    event.add('dtstamp', datetime.now())
    event['uid'] = uuid.uuid4().hex
    cal.add_component(event)


table = soup.find_all('table')
# Skip header
for tr in table[0].find_all('tr')[1:]:
    tds = tr.find_all('td')
    col_data = ['\n'.join([y.get_text() for y in x.find_all('span')]) for x in tds]
    if ' - ' not in col_data[1]:
        continue

    start, end = col_data[1].split(' - ')
    start = datetime.strptime('2017 ' + start, '%Y %m/%d').date()
    d_m, d_t, d_w, d_r, d_f, d_s = [start + timedelta(days=i) for i in range(6)]

    if len(col_data) == 4:
        start_end = col_data[1]
        week = col_data[3]
        add_event(
            d_m,
            d_s,
            week,
        )

    # event.add('dtstamp', datetime(2005,4,4,0,10,0,tzinfo=UTC))
    else:
        start_end = col_data[1]
        tuesday = col_data[3]
        thursday = col_data[4]
        friday = col_data[5]

        if len(tuesday) > 0:
            add_event(
                datetime.combine(d_t, time(11, 10)),
                datetime.combine(d_t, time(12, 25)),
                tuesday
            )
        if len(thursday) > 0:
            add_event(
                datetime.combine(d_r, time(11, 10)),
                datetime.combine(d_r, time(12, 25)),
                thursday
            )

        if len(friday) > 0:
            add_event(
                datetime.combine(d_f, time(9)),
                datetime.combine(d_f, time(11)),
                friday
            )
            add_event(
                datetime.combine(d_f, time(13)),
                datetime.combine(d_f, time(15)),
                friday
            )

        # print(tuesday)

f = open('calendar.ics', 'wb')
f.write(cal.to_ical())
f.close()
