# osx_cal_list_events.py

This Python script lists the events in the macOS Calendar app.
By default, it will list the events for the next week, in the "Home" calendar,
but you can specify a different calendar and/or a different time period.

Author: Brett Hutley <brett@hutley.net>

## Installation

The script requires the `pyobjc` package. Install it with the following command:

```bash
pip3 install pyobjc
```

## Usage

The script accepts the following arguments:

<pre>
options:
  -h, --help            show this help message and exit
  -s START_DATE, --start-date START_DATE
                        Start date of period to list
  -e END_DATE, --end-date END_DATE
                        End date of period of list
  -c CALENDAR, --calendar CALENDAR
                        Calendar to add event to. Default is "Home"
</pre>

The script accepts dates in the following formats:

- YYYY-mm-dd - a plain date without time information.
- YYYY-mm-ddTHH:MM - A YMD with a time.
- YYYY-mm-dd HH:MM - A YMD with a time.

If no start date is specified, the script will default to the current date.
If no end date is specified, the script will default to the start date + 7 days.
If no calendar is specified, the script will default to the "Home" calendar.
