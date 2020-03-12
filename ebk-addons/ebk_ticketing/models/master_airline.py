# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

# ducngo
# 16DEC19


class MasterAirline(models.Model):

    _name = "ticketing.master.airline"
    _rec_name = "airline"
    airline = fields.Char(string='Hãng hàng không')
    image = fields.Image(string='Logo')
    code = fields.Char(string='Mã hiệu')
