# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date


class TopupSupplier(models.TransientModel):
    _name = "topup.supplier"
    customer_id = fields.Many2one(
        'res.partner', string=_("Supplier"), required=True, domain=[('topup_type', '=', 'supplier')])
    bank_id = fields.Many2one('res.partner', string=_(
        "Bank"), domain=[('topup_type', '=', 'bank')])
    bank_type = fields.Selection(
        [('invidual', _('Invidual Bank')), ('company', _('Company Bank'))], string=_('Bank Type'))
    money = fields.Float(string=_("Money"))
    trans_fee = fields.Float(string=_("Transfer Fee"))
    notes = fields.Text(string=_("Note"))

    def create_topup_supplier(self):

        # increase supplier's balance
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

        # decrease bank's balance
        trans_customer_id = self.bank_id.id
        trans_code = "TOPUP"
        money = -1 * self.money
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

        # decrease bank's balance by fee
        if self.trans_fee > 0:
            trans_customer_id = self.bank_id.id
            trans_code = "TOPUP"
            money = -1 * self.trans_fee
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

        # decrease cost' balance
        if self.trans_fee > 0:
            ICPSudo = self.env['ir.config_parameter'].sudo()
            account_cost_id = ICPSudo.get_param(
                'ebk_ticketing.account_cost')

            trans_customer_id = account_cost_id
            trans_code = "TOPUP"
            money = -1 * self.trans_fee
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
