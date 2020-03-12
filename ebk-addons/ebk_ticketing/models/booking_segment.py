# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

# ducngo
# 16DEC19


class BookingSegment(models.Model):
    _name = 'ticketing.booking.segment'
    booking_id = fields.Many2one('ticketing.booking', string='Booking ID')

    # Mã hành trình
    # Hãng
    airline_id = fields.Many2one(
        'ticketing.master.airline', string='Hãng hàng không', required=True)
    # Loại máy bay
    aircraft = fields.Char(string='Loại máy bay')
    # Nhà cung cấp
    supplier_id = fields.Many2one('res.partner', string='Nhà cung cấp')
    # Loại hành trình
    type_way = fields.Selection(
        [('dep', 'Chiều đi'), ('ret', 'Chiều về')], string='Loại hành trình', required=True)
    # Số hiệu
    flight_number = fields.Char(string='Số hiệu', required=True)
    # Hạng vé
    flight_class = fields.Char(string='Hạng vé', required=True)
    # Xuất phát
    airport_departure = fields.Many2one(
        'ticketing.master.airport', string='Sân bay đi', required=True)
    # Nơi đến
    airport_arrival = fields.Many2one(
        'ticketing.master.airport', string='Sân bay đến', required=True)
    # Thời gian bắt đầu
    flight_date_departure = fields.Datetime(string='Giờ đi', required=True)
    # Thời gian kết thúc
    flight_date_arrival = fields.Datetime(string='Giờ đến', required=True)
    # Thời gian bay
    flight_during_time = fields.Integer(string='Thời gian bay')
    # Cổng đi
    gate_departure = fields.Char(string='Cổng đi')
    # Cổng đến
    gate_arrival = fields.Char(string='Cổng đến')
