#!/usr/bin/env python3
"""
A script to list events in an OS/X Calendar.

Written by Brett Hutley <brett@hutley.net>
"""
from typing import Optional
import objc
import argparse
from EventKit import EKEventStore, EKEntityTypeEvent, EKCalendar, EKEvent, EKSpanThisEvent
from Foundation import NSDate

import datetime


def parse_date(date_str: str) -> datetime.datetime:
    """Parse a date string in the format YYYY-MM-DD, YYYY-MM-DDTHH:MM, or YYYY-MM-DD HH:MM.
    """
    date_str = date_str.strip()

    if 'T' in date_str or ' ' in date_str:
        parse_format = "%Y-%m-%dT%H:%M" if 'T' in date_str else "%Y-%m-%d %H:%M"
    else:
        parse_format = "%Y-%m-%d"
    return datetime.datetime.strptime(date_str, parse_format)


def datetime_to_nsdate(dt: datetime.datetime) -> NSDate:
    return NSDate.dateWithTimeIntervalSince1970_(dt.timestamp())


def nsdate_to_datetime(nsdate: NSDate) -> datetime.datetime:
    return datetime.datetime.fromtimestamp(nsdate.timeIntervalSince1970())


def resolve_calendar_by_name(store: EKEventStore, calendar_name: str) -> Optional[EKCalendar]:
    calendars = store.calendarsForEntityType_(EKEntityTypeEvent)
    for cal in calendars:
        if cal.title() == calendar_name:
            return cal
    return None


if __name__ == "__main__":
    objc.options.verbose = True

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-s', '--start-date', type=str, required=False, default="", help='Start date of period to list')
    parser.add_argument('-e', '--end-date', type=str, required=False, default="", help='End date of period of list')
    parser.add_argument('-c', '--calendar', type=str, required=False, default="Home",
                        help='Calendar to add event to. Default is "Home"')
    args = parser.parse_args()

    # Create an event store object
    store = EKEventStore.alloc().init()

    home_cal = resolve_calendar_by_name(store, args.calendar)
    if home_cal is None:
        print(f"Couldn't find a calendar with the name: {args.calendar}")
        print("Available calendars:")
        calendars = store.calendarsForEntityType_(EKEntityTypeEvent)
        for cal in calendars:
            print(f"  {cal.title()} ({cal.type()})")
        exit(1)

    empty = lambda x: True if x is None or len(x) == 0 else False
    start_date = parse_date(args.start_date) if not empty(args.start_date) else datetime.datetime.now()
    end_date = parse_date(args.end_date) if not empty(args.end_date) else start_date + datetime.timedelta(days=7)
    start_date_nsdate = datetime_to_nsdate(start_date)
    end_date_nsdate = datetime_to_nsdate(end_date)
    pred = store.predicateForEventsWithStartDate_endDate_calendars_(start_date_nsdate, end_date_nsdate, [home_cal])
    events = store.eventsMatchingPredicate_(pred)
    for event in events:
        ev_start_date = nsdate_to_datetime(event.startDate())
        ev_end_date = nsdate_to_datetime(event.endDate())
        ev_all_day = event.isAllDay()
        ev_has_notes = event.hasNotes()
        ev_notes = event.notes() if ev_has_notes else ""
        print(f"{ev_start_date.strftime('%Y-%m-%dT%H:%M')}\t{ev_end_date.strftime('%Y-%m-%dT%H:%M')}\t{event.title()}\t{ev_notes}")

