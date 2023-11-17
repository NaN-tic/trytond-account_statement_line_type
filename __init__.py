from . import statement
from trytond.pool import Pool

def register():
    Pool.register(
        statement.Type,
        statement.Line,
        module="account_statement_line_type", type_="model")
