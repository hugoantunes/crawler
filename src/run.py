#!/usr/bin/python

import sys
import getopt
from crawler import Crawler


def main(argv):
    url = ''
    try:
        opts, args = getopt.getopt(argv, "hu:", ["url="])
    except getopt.GetoptError:
        print 'test.py -u <url>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'test.py -u <url>'
            sys.exit()
        elif opt in ("-u", "--url"):
            url = arg

    crawler = Crawler(url=url)
    crawler.get_all_resources()
    print crawler.resources

if __name__ == "__main__":
    main(sys.argv[1:])
