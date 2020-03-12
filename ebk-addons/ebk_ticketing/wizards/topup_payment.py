# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date


class TopupPayment(models.TransientModel):
    _name = "topup.payment"
    customer_id = fields.Many2one(
        'res.partner', string=_("Customer"), required=True, domain=[('topup_type', '=', 'agent')])
    supplier_id = fields.Many2one('res.partner', required=True, string=_(
        "Supplier"), domain=[('topup_type', '=', 'supplier')])
    code = fields.Char(string=_("Code"), required=True)
    money = fields.Float(string=_("Money"), required=True)
    payment_fee = fields.Float(string=_("Transfer Fee"))
    supplier_fee = fields.Float(string=_("Supplier Fee"))
    notes = fields.Text(string=_("Note"))

    def create_topup_payment(self):

        # increase supplier's balance
        trans_customer_id = self.supplier_id.id
        trans_code = self.code
        money = -1*self.money
        notes = self.notes

        vals = {
            "customer_id": trans_customer_id,
            "code": trans_code,
            "date": trans_code,
            "money": money,
            "notes": notes,
            "transaction_type": "payment"
        }

        self.env['ticketing.transaction'].create(vals)

        # decrease customer's balance
        trans_customer_id = self.customer_id.id
        money = -1 * self.money
        notes = self.notes

        vals = {
            "customer_id": trans_customer_id,
            "code": trans_code,
            "date": trans_code,
            "money": money,
            "notes": notes,
            "transaction_type": "payment"
        }

        self.env['ticketing.transaction'].create(vals)

        if self.payment_fee > 0:
            # decrease customer's balance by fee
            trans_customer_id = self.customer_id.id
            money = -1 * self.payment_fee
            notes = self.notes

            vals = {
                "customer_id": trans_customer_id,
                "code": trans_code,
                "date": trans_code,
                "money": money,
                "notes": notes,
                "transaction_type": "payment"
            }

            self.env['ticketing.transaction'].create(vals)

            # encrease profit' balance
            ICPSudo = self.env['ir.config_parameter'].sudo()
            account_profit = ICPSudo.get_param(
                'ebk_ticketing.account_profit')

            trans_customer_id = int(account_profit)
            money = self.payment_fee
            notes = self.notes

            vals = {
                "customer_id": trans_customer_id,
                "code": trans_code,
                "date": trans_code,
                "money": money,
                "notes": notes,
                "transaction_type": "payment"
            }

            self.env['ticketing.transaction'].create(vals)

        if self.supplier_fee > 0:
            # decrease supplier's balance by fee
            trans_customer_id = self.supplier_id.id
            money = -1 * self.supplier_fee
            notes = self.notes

            vals = {
                "customer_id": trans_customer_id,
                "code": trans_code,
                "date": trans_code,
                "money": money,
                "notes": notes,
                "transaction_type": "payment"
            }

            self.env['ticketing.transaction'].create(vals)

            # encrease cost' balance
            ICPSudo = self.env['ir.config_parameter'].sudo()
            account_cost = ICPSudo.get_param(
                'ebk_ticketing.account_cost')

            trans_customer_id = int(account_cost)
            money = -1*self.supplier_fee
            notes = self.notes

            vals = {
                "customer_id": trans_customer_id,
                "code": trans_code,
                "date": trans_code,
                "money": money,
                "notes": notes,
                "transaction_type": "payment"
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
