# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.tests.test_tryton import ModuleTestCase


class StatementLineTypeTestCase(ModuleTestCase):
    'Test Statement Line Type module'
    module = 'account_statement_line_type'

del ModuleTestCase
