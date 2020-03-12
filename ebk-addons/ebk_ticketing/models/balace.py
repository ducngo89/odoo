# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class TicketingBalance(models.Model):
    _name = "ticketing.balance"
    _description = "Balance Record"

    customer_id = fields.Many2one(
        'res.partner', string=_("Account"), required=True)
    balance = fields.Float(string=_("Money"), required=True)
    account_type = fields.Char(
        string=_("Account Type"))
    last_date = fields.Datetime(string=_("Date"), required=True)

    @api.model
    def create(self, vals):
        vals["account_type"] = self.env['res.partner'].search(
            [('id', '=', vals['customer_id'])]).topup_type
        result = super(TicketingBalance, self).create(vals)
        return result


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    topup_type = fields.Selection([
        ('agent', _("Agent")),
        ('bank', _("Banks")),
        ('profit', _("Profit")),
        ('supplier', _("Supplier")),
        ('cost', _("Cost"))], string=_("Topup Type"))
