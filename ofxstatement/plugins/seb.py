# -*- coding: utf-8 -*-

import re
import itertools
import logging

from datetime import datetime
from openpyxl import load_workbook

from ofxstatement.parser import StatementParser
from ofxstatement.plugin import Plugin
from ofxstatement.statement import Statement, StatementLine, generate_transaction_id


def take(n, iterable):
    """Return first n items of the iterable as a list."""
    return list(itertools.islice(iterable, n))


class SebStatementParser(StatementParser):
    date_format = '%Y-%m-%d'
    bank_id = 'SEB'
    currency_id = 'SEK'
    header_regexp = '^Datum: ([0-9]{4}-[0-9]{2}-[0-9]{2}) - ([0-9]{4}-[0-9]{2}-[0-9]{2})$'

    def __init__(self, fin, clean=False):
        """
        Create a new SebStatementParser instance.

        :param fin: filename to create parser for
        :param clean: whenever to attempt to clean description
        """

        self.workbook = load_workbook(filename=fin, read_only=True)
        self.clean = clean

        self.validate()
        self.statement = self.parse_statement()

    def validate(self):
        """
        Naive validation to make sure that xlsx document is structured the way it was
        when this parser was written.

        :raises ValueError if workbook has invalid format
        """

        sheet = self.workbook.active
        try:
            logging.info('Checking that sheet has at least 5 rows.')
            rows = take(5, sheet.iter_rows())
            assert len(rows) == 5

            logging.info('Extracting values for every cell.')
            rows = [[c.value for c in row] for row in rows]

            logging.info('Verifying summary header.')
            row = rows[0]
            assert ['Saldo', 'Disponibelt belopp', 'Beviljad kredit', None, None] == row[1:]

            logging.info('Detecting accounts.')
            accounts = 0
            idx = 1
            while not re.match(SebStatementParser.header_regexp, rows[idx][0]):
                account_id = rows[idx][0]
                logging.info('Detected account: %s' % account_id)
                accounts += 1
                idx += 1
            logging.info('Total (%s) accounts detected.' % accounts)
            assert accounts == 1

            logging.info('Verifying summary footer.')
            row = rows[idx]
            assert re.match(SebStatementParser.header_regexp, row[0])
            assert [None, None, None, None, None] == row[1:]
            idx += 1

            logging.info('Skipping empty/padding row.')
            row = rows[idx]
            assert [None, None, None, None, None, None] == row
            idx += 1

            logging.info('Verifying statements header.')
            row = rows[idx]
            assert re.match('^Bokföringsdatum$', row[0])
            assert re.match('^Valutadatum$', row[1])
            assert re.match('^Verifikationsnummer$', row[2])
            assert re.match('^Text / mottagare$', row[3])
            assert re.match('^Belopp$', row[4])
            assert re.match('^Saldo$', row[5])

            logging.info('Everything is OK!')

        except AssertionError as e:
            raise ValueError(e)

    def parse_statement(self):
        """
        Parse information from xlsx header that could be used to populate statement.

        :return: statment object
        """

        statement = Statement()
        sheet = self.workbook.active

        # We need only first 2 rows here.
        rows = take(3, sheet.iter_rows())
        rows = [[c.value for c in row] for row in rows]

        values = rows[1]
        privatkonto, saldo, disponibelt_belopp, beviljad_kredit, _1, _2 = values
        statement.account_id = privatkonto
        statement.end_balance = float(saldo)
        statement.bank_id = self.bank_id
        statement.currency = self.currency_id

        header = rows[2]
        m = re.match(self.header_regexp, header[0])
        if m:
            part_from, part_to = m.groups()
            statement.start_date = self.parse_datetime(part_from)
            statement.end_date = self.parse_datetime(part_to)

        return statement

    def split_records(self):
        sheet = self.workbook.active

        # Skip first 5 rows. Headers they are.
        for row in itertools.islice(sheet.iter_rows(), 5, None):
            # Row is potentially big so we yield generator.
            yield (c.value for c in row)

    def parse_record(self, row):
        row = take(5, row)

        stmt_line = StatementLine()
        stmt_line.date = self.parse_datetime(row[0])
        _ = self.parse_datetime(row[1])  # TODO: ???
        stmt_line.refnum = row[2]
        stmt_line.memo = row[3]
        stmt_line.amount = row[4]

        #
        # Looks like SEB formats description for card transactions so it includes the actual purchase date
        # within e.g. 'WIRSTRÖMS PU/14-12-31' and it means that description is 'WIRSTRÖMS PU' while the actual
        # card operation is 2014-12-31.
        #
        # P.S. Wirströms Irish Pub is our favorite pub in Stockholm.
        #
        if self.clean:
            m = re.match('(.*)/([0-9]{2}-[0-9]{2}-[0-9]{2})$', stmt_line.memo)
            if m:
                stmt_line.memo, date_string = m.groups()
                stmt_line.date_user = datetime.strptime(date_string, '%y-%m-%d')

        stmt_line.id = generate_transaction_id(stmt_line)
        return stmt_line


class SebPlugin(Plugin):
    def get_parser(self, fin):
        return SebStatementParser(fin)
