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

    week_start = datetime.date.today()
    date_format = "%a, %b %d"

    if options.startdate is not None:
        week_start = datetime.datetime.strptime(options.startdate, "%Y-%m-%d").date()

    week_delta = datetime.timedelta(days=7)
    for _ in xrange(options.weeks):
        for i in [1,3]:
            d = week_start + datetime.timedelta(days=i)
            print "## {0}".format(d.strftime(date_format))
            print
            print

        week_start += week_delta



if __name__ == '__main__':
    main()
