#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os.path
import click

from ofxstatement.ofx import OfxWriter
from ofxstatement.plugins import seb


@click.command()
@click.argument('path')
@click.option('--debug', is_flag=True, default=False)
def convert(path, debug):
    """Parse and print transactions from SEB Export.xlsx file."""

    root, ext = os.path.splitext(path)
    output_file = root + '.ofx'

    parser = seb.SebPlugin(ui=None, settings=None).get_parser(path)
    statement = parser.parse()

    if debug:
        for line in statement.lines:
            print(line)
        return

    with open(output_file, 'w') as out:
        writer = OfxWriter(statement)
        out.write(writer.toxml())


if __name__ == '__main__':
    convert()
