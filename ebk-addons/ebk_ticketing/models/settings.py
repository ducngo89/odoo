# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class TopupSettings(models.TransientModel):
    _inherit = "res.config.settings"

    account_profit = fields.Many2one(
        'res.partner', string=_("Account Frofit"), required=True)
    account_cost = fields.Many2one(
        'res.partner', string=_("Account Cost"), required=True)

    def set_values(self):
        res = super(TopupSettings, self).set_values()
        self.env['ir.config_parameter'].set_param(
            'ebk_ticketing.account_profit', self.account_profit.id)

        self.env['ir.config_parameter'].set_param(
            'ebk_ticketing.account_cost', self.account_cost.id)

        print('Save profit config: ', self.account_profit.id)
        print('Save cost config: ', self.account_cost.id)

        return res

    @api.model
    def get_values(self):
        res = super(TopupSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()

        account_profit_id = ICPSudo.get_param('ebk_ticketing.account_profit')
        res.update(
            account_profit=int(account_profit_id)
        )

        account_cost_id = ICPSudo.get_param('ebk_ticketing.account_cost')
        res.update(
            account_cost=int(account_cost_id)
        )

        print('Get profit config: ', account_profit_id)
        print('Get cost config: ', account_cost_id)

        return res
