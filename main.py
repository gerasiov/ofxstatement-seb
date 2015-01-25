#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import seb

from ofxstatement.ofx import OfxWriter


def main(args=None):
    parser = argparse.ArgumentParser(
        description='Parse and print transactions from SEB export xlsx file.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('path', help='path to the xlsx file')
    opts = parser.parse_args(args)

    parser = seb.SebPlugin(None, None).get_parser(opts.path)
    statement = parser.parse()
    with open('output', 'w') as out:
        writer = OfxWriter(statement)
        out.write(writer.toxml())

if __name__ == '__main__':
    main()
