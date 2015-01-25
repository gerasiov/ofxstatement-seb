#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import seb
import os.path

from ofxstatement.ofx import OfxWriter


def main(args=None):
    parser = argparse.ArgumentParser(
        description='Parse and print transactions from SEB export xlsx file.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('path', help='path to the xlsx file')
    opts = parser.parse_args(args)

    input_file = opts.path
    root, ext = os.path.splitext(input_file)
    output_file = root + '.ofx'
    parser = seb.SebPlugin(None, None).get_parser(opts.path)
    statement = parser.parse()
    with open(output_file, 'w') as out:
        writer = OfxWriter(statement)
        out.write(writer.toxml())

if __name__ == '__main__':
    main()
