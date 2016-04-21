.. image:: https://travis-ci.org/themalkolm/ofxstatement-seb.svg?branch=master
    :target: https://travis-ci.org/themalkolm/ofxstatement-seb

This is a collection of parsers for proprietary statement formats, produced by
`SEB`_. It parses ``Export.xlsx`` file exported from internet bank.

It is a plugin for `ofxstatement`_.

.. _SEB: http://seb.se
.. _ofxstatement: https://github.com/kedder/ofxstatement

Configuration
=============

There is only one configuration option ``brief``. Turn it on if you want to parse description
and replace it with the actual card description while stripping off any know additional
data e.g:

``WIRSTRÖMS PU/14-12-31`` -> ``WIRSTRÖMS PU``

Sample configuration file::

    [seb]
    plugin = seb
    brief = 1
