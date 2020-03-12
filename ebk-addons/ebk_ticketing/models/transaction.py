# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date


class TicketingTransaction(models.Model):
    _name = "ticketing.transaction"
    _description = "Transaction Record"
    _order = "id desc"

    customer_id = fields.Many2one(
        'res.partner', string=_("Account"), required=True)
    code = fields.Char(string=_("Code"), required=True)
    date = fields.Datetime(string=_("Date"), required=True,
                           default=lambda self: date.today())
    money = fields.Float(string=_("Money"), required=True)
    money_after = fields.Float(string=_("Money After"))
    notes = fields.Text(string=_("Note"))
    transaction_type = fields.Selection([('topup', 'TOPUP'), ('payment', 'PAY'), (
        'ck', 'CK'), ('other', 'OTHER')], string="Transaction Type")

    @api.model
    def create(self, vals):
        print('Add new record transaction: ', vals)

        balance = self.env['ticketing.balance'].search(
            [('customer_id', '=', int(vals["customer_id"]))])

        if balance:
            balance.balance += vals["money"]
            vals["money_after"] = balance.balance
        else:
            balance_vals = {
                "customer_id": vals["customer_id"],
                "last_date": date.today(),
                "balance": vals["money"],
            }
            self.env['ticketing.balance'].create(balance_vals)
            vals["money_after"] = vals["money"]

        vals['date'] = date.today()
        result = super(TicketingTransaction, self).create(vals)
        return result
