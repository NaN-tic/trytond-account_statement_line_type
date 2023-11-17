from . import statement
from trytond.pool import Pool

def register():
    Pool.register(
        statement.Type,
        statement.Line,
        module="Minimitzar errors en la introducció de despeses en els extractes", type_="model")
