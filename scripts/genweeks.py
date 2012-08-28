#!/usr/bin/env python


import datetime
import optparse


def main():
    """
    """
    parser = optparse.OptionParser()
    parser.add_option("-s", dest="startdate", type="string", default=None, help="Start Date (YYYY-MM-DD)")
    parser.add_option("-w", dest="weeks", type="int", default="16", help="Number of Weeks")
    parser.add_option("-a", dest="abbrev", action="store_true", default=True, help="Abbreviate Month")
    (options, args) = parser.parse_args()

    begin = datetime.date.today()
    date_format = "%B %d"

    if options.abbrev:
        date_format = "%b %d"

    if options.startdate is not None:
        begin = datetime.datetime.strptime(options.startdate, "%Y-%m-%d").date()

    end = begin + datetime.timedelta(days=6)


    week_delta = datetime.timedelta(days=7)
    for _ in xrange(options.weeks):
        print "{0} -- {1}".format(begin.strftime(date_format), end.strftime(date_format))
        begin += week_delta
        end += week_delta



if __name__ == '__main__':
    main()
