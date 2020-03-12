# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

# ducngo
# 16DEC19


class BookingAddon(models.Model):
    _name = 'ticketing.booking.addon'
    booking_id = fields.Many2one('ticketing.booking', string='Booking ID')
    # Tên dịch vụ
    addon = fields.Char(string='Dịch vụ cộng thêm')
    # Hành khách
    passenger_id = fields.Many2one(
        'ticketing.passenger', string='Tìm hành khách')
    passenger_name = fields.Char(string='Hành khách', required=True)
    # Giá trị
    value = fields.Char(string='Giá trị', required=True)
    # Loại tiền tệ
    currency_id = fields.Many2one(
        "res.currency", string="Tiền tệ", required=True)
    # Thành tiền
    money = fields.Float(string='Thành tiền', required=True)
    # Mã chuyến bay
    flight_no = fields.Char(string='Mã chuyến bay', required=True)
    @api.onchange('passenger_id')
    def passenger_select(self):
        self.passenger_name = self.passenger_id.fullname
