# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date


class TopupTransfer(models.TransientModel):
    _name = "topup.transfer"
    customer_from = fields.Many2one(
        'res.partner', string=_("Account From"), required=True)
    customer_to = fields.Many2one(
        'res.partner', string=_("Account To"), required=True)
    money = fields.Float(string=_("Money"))
    money_fee = fields.Float(string=_("Money Fee"))
    notes = fields.Text(string=_("Note"))

    def create_topup_transfer(self):

        # decrease from's balance
        customer_id = self.customer_from.id
        trans_code = "CK"
        money = -1*self.money
        notes = self.notes

        vals = {
            "customer_id": customer_id,
            "code": trans_code,
            "money": money,
            "notes": notes,
            "transaction_type": "ck"
        }

        self.env['ticketing.transaction'].create(vals)

        # encrease to's balance
        customer_id = self.customer_to.id
        trans_code = "CK"
        money = self.money
        notes = self.notes

        vals = {
            "customer_id": customer_id,
            "code": trans_code,
            "money": money,
            "notes": notes,
            "transaction_type": "ck"
        }

        self.env['ticketing.transaction'].create(vals)

        if self.money_fee > 0:
            # decrease from's balance fee
            customer_id = self.customer_from.id
            trans_code = "CK"
            money = -1*self.money_fee
            notes = self.notes

            vals = {
                "customer_id": customer_id,
                "code": trans_code,
                "money": money,
                "notes": notes,
                "transaction_type": "ck"
            }

            self.env['ticketing.transaction'].create(vals)

            # encrease cost's balance fee
            ICPSudo = self.env['ir.config_parameter'].sudo()
            account_cost = ICPSudo.get_param(
                'ebk_ticketing.account_cost')

            customer_id = int(account_cost)
            trans_code = "CK"
            money = -1*self.money_fee
            notes = self.notes

            vals = {
                "customer_id": customer_id,
                "code": trans_code,
                "money": money,
                "notes": notes,
                "transaction_type": "ck"
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
