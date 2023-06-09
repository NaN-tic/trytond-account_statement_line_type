# This file is part statement_line_types module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import statement

def register():
    Pool.register(
        statement.Type,
        statement.Line,
        module='account_statement_line_type', type_='model')
