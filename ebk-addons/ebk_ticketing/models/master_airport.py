# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

# ducngo
# 16DEC19


class MasterAirport(models.Model):

    _name = "ticketing.master.airport"
    _rec_name="code"
    code = fields.Char(string='Mã sân bay')
    country_id = fields.Many2one('res.country', 'Quốc gia')
    state_id = fields.Many2one('res.country.state', 'Thành phố')
    street = fields.Char(string='Địa chỉ')
    image = fields.Image(string='Hình ảnh')
