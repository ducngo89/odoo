# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date


class TopupAgent(models.TransientModel):
    _name = "topup.agent"
    customer_id = fields.Many2one(
        'res.partner', string=_("Account"), required=True, domain=[('topup_type', '=', 'agent')])
    bank_id = fields.Many2one('res.partner', string=_(
        "Bank"), domain=[('topup_type', '=', 'bank')])
    money = fields.Float(string=_("Money"))
    notes = fields.Text(string=_("Note"))

    def create_topup_agent(self):

        # increase angent's balance
        trans_customer_id = self.customer_id.id
        trans_code = "TOPUP"
        money = self.money
        notes = self.notes

        vals = {
            "customer_id": trans_customer_id,
            "code": trans_code,
            "date": trans_code,
            "money": money,
            "notes": notes,
            "transaction_type": "topup"
        }

        self.env['ticketing.transaction'].create(vals)

        # increase bank's balance
        trans_customer_id = self.bank_id.id
        trans_code = "TOPUP"
        money = self.money
        notes = self.notes

        vals = {
            "customer_id": trans_customer_id,
            "code": trans_code,
            "date": trans_code,
            "money": money,
            "notes": notes,
            "transaction_type": "topup"
        }

        self.env['ticketing.transaction'].create(vals)
        return {
            'name': 'Lịch sử giao dịch',
            # 'domain': [('patient_id', '=', self.id)],
            'view_type': 'form',
            'res_model': 'ticketing.transaction',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }
