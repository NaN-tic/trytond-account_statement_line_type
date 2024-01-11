from trytond.model import ModelSQL, ModelView, fields
from trytond.pool import PoolMeta, Pool
from trytond.transaction import Transaction
from trytond.pyson import Eval, Id


class Type(ModelSQL, ModelView):
    'Statement Line Type'
    __name__ = 'account.statement.line.type'
    name = fields.Char('Name', required=True)
    company = fields.Many2One('company.company', 'Company', required=True)
    account = fields.Many2One('account.account', 'Account', required=True,
        domain=[
            ('company', '=', Eval('company', 0)),
            ('type', '!=', None),
            ('closed', '!=', True),
            ])

    @classmethod
    def default_company(cls):
        return Transaction().context.get('company')


class Line(metaclass=PoolMeta):
    __name__ = 'account.statement.line'
    type = fields.Many2One('account.statement.line.type', 'Type', required=True,
        domain=[
            ('company', '=', Eval('company', 0)),
            ])

    @classmethod
    def __setup__(cls):
        super().__setup__()
        cls.account.states['invisible'] = ~Eval('context', {}).get('groups',
            []).contains(Id('account', 'group_account'))

    @classmethod
    def create(cls, vlist):
        vlist = vlist[:]
        for values in vlist:
            values.update(cls.update_type(values))
        return super().create(vlist)

    @classmethod
    def write(cls, *args):
        if args[0]:
            actions = iter(args)
            args = []
            for lines, values in zip(actions, actions):
                for line in lines:
                    args.append([line])
                    args.append(cls.update_type(values, line))
        super().write(*args)

    @classmethod
    def update_type(cls, values, record=None):
        Type = Pool().get('account.statement.line.type')
        values = values.copy()
        if values.get('type'):
            values['account'] = Type(values.get('type')).account.id
        elif values.get('account') and not record:
            types = Type.search([('account', '=', values['account'])], limit=1)
            if types:
                values['type'], = types
        return values

    @fields.depends('type')
    def on_change_type(self):
        if not self.type:
            self.account = None
            return
        self.account = self.type.account
