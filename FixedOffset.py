#class for fixing time offsets
#from https://docs.python.org/2/library/datetime.html#datetime.tzinfo.fromutc

import datetime
from datetime import timedelta, tzinfo

def parseISOTime(t):
  time_str = t
  # split the utc offset part
  naive_time_str, offset_str = time_str[:-6], time_str[-6:]
  # parse the naive date/time part
  naive_dt = datetime.datetime.strptime(naive_time_str, '%Y-%m-%dT%H:%M:%S')
  # parse the utc offset
  offset = int(offset_str[-5:-3])*60 + int(offset_str[-2:])
  if offset_str[0] == "-":
    offset = -offset
  dt = naive_dt.replace(tzinfo=FixedOffset(offset))
  return dt

class FixedOffset(tzinfo):
    """Fixed offset in minutes: `time = utc_time + utc_offset`."""
    def __init__(self, offset):
        self.__offset = timedelta(minutes=offset)
        hours, minutes = divmod(offset, 60)
        #NOTE: the last part is to remind about deprecated POSIX GMT+h timezones
        #  that have the opposite sign in the name;
        #  the corresponding numeric value is not used e.g., no minutes
        self.__name = '<%+03d%02d>%+d' % (hours, minutes, -hours)
    def utcoffset(self, dt=None):
        return self.__offset
    def tzname(self, dt=None):
        return self.__name
    def dst(self, dt=None):
        return timedelta(0)
    def __repr__(self):
        return 'FixedOffset(%d)' % (self.utcoffset().total_seconds() / 60)