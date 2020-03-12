# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

# ducngo
# 16DEC19


class BookingPrice(models.Model):
    _name = 'ticketing.booking.price'
    booking_id = fields.Many2one('ticketing.booking', string='Booking ID')

    # Loại hành trình
    type_way = fields.Selection(
        [('dep', 'Chiều đi'), ('ret', 'Chiều về')], string='Loại hành trình', required=True)
    # Mã hành khách
    passenger_id = fields.Many2one(
        'ticketing.passenger', string="Tìm hành khách")
    # Loại giá
    price_type = fields.Char(string="Loại giá")
    passenger_name = fields.Char(string="Hành khách", required=True)
    # Mô tả
    notes = fields.Char(string="Mô tả")
    # Số tiền (Trước thuế)
    price_amount = fields.Float(string="Giá", required=True)
    # Loại tiền tệ
    currency_id = fields.Many2one(
        "res.currency", string="Tiền tệ", required=True)
    # VAT
    price_vat = fields.Float(string="Thuế", required=True)
    # Tổng cộng (Sau thuế)
    price_after = fields.Float(
        string='Thành tiền', readonly=True, required=True)

    @api.onchange('price_amount', 'price_vat')
    def set_total_price(self):
        print('price change')
        self.price_after = self.price_amount + self.price_vat

    @api.onchange('passenger_id')
    def passenger_select(self):
        self.passenger_name = self.passenger_id.fullname
