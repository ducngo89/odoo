# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Location(models.Model):
    _name = 'ticketing.master.location'
    _rec_name = "location"

    location = fields.Char(string="Địa điểm")
    code = fields.Char(string="Mã địa điểm")
    state_id = fields.Many2one('res.country.state', string="Tỉnh/thành")
    country_id = fields.Many2one('res.country', string="Quốc gia")
