# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductInherit(models.Model):
    _inherit = 'product.template'
    is_transport = fields.Boolean(string='Là vé tàu/xe')

    location_departure = fields.Many2one(
        'ticketing.master.location', string='Điểm xuất phát')
    location_arrival = fields.Many2one(
        'ticketing.master.location', string='Điểm đến')
