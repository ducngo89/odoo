# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

# ducngo
# 16DEC19


class Booking(models.Model):

    _name = "ticketing.booking"
    _rec_name = "booking_pnr"
    _inherit = ['mail.thread.cc', 'mail.activity.mixin']
    _description ="Booking model"
    # Mã booking - Autogen by odoo
    # Mã booking củ
    parent_booking_id = fields.Many2one(
        "ticketing.booking", string="Mã booking")
    # Mã code
    booking_pnr = fields.Char(string="Mã đặt chỗ", required=True)
    # Tổng Số lượng vé
    total_tickets = fields.Integer(string="Số lượng vé")
    # Tổng Giá bán
    total_price_amount = fields.Float(string="Tổng tiền")
    # Loại tiền tệ
    currency_id = fields.Many2one("res.currency", string="Tiền tệ")
    # Giá gôc
    total_price_net = fields.Float(string="Giá gốc")
    # Hành trình
    sector = fields.Char(string="Hành trình")
    # Loại hành trình, ow, rt
    type_way = fields.Selection(
        [('ow', 'Một chiều'), ('rt', 'Khứ hồi')], string="Loại hành trình")
    contact_id = fields.Many2one("res.partner", "Liên hệ")
    # Tên liên hệ
    contact_name = fields.Char(
        string="Tên liên hệ", required=True)
    # Địa chỉ liên lạc
    contact_address = fields.Char(
        string="Địa chỉ liên hệ", required=True)
    # Số điện thoại
    contact_phone = fields.Char(
        string="Số điện thoại", required=True)
    # Email liên hệ
    contact_email = fields.Char(
        string="Email", required=True)
    # Người book
    booker = fields.Many2one("res.partner", "Người đặt chỗ", required=True)
    # Người xuất vé
    confirm_user = fields.Many2one("res.partner", "Người xuất vé")
    # Ngày book ~ ngày tạo  - create_date

    # Trạng thái booking
    state = fields.Selection(
        [('draft', 'Nháp'),
         ('book', 'Đang giữ chỗ'),
         ('book_error', 'Lỗi đặt chỗ'),
         ('timeout', 'Hết hạn thanh toán'),
         ('confirm_error', 'Lỗi xuất vé'),
         ('confirm', 'Đã xuất vé'),
         ], string="Trạng thái booking")
    # Hình thức thanh toán
    payment_type = fields.Selection(
        [('agent', 'Tài khoản đại lý'),
         ('later', 'Thanh toán sau'),
         ('online', 'Thanh toán trực tuyến'),
         ], string="Hình thức thanh toán")
    # Trạng thái thanh toán
    payment_status = fields.Selection([('notpaid', 'Chưa thanh toán'),
                                       ('paid_litle', 'Đã thanh toán một phần'),
                                       ('paid_all', 'Đã thanh toán'),
                                       ], string="Trạng thái thanh toán")
    # Ngày thanh toán
    paid_date = fields.Datetime(string="Ngày thanh toán")
    # Ngày xuất vé
    confirm_date = fields.Datetime(string="Ngày xuất vé")
    # Hạn giữ chỗ
    hold_date = fields.Datetime(string="Hạn giữ chỗ")
    # Thực thu
    paid_amount = fields.Float(string="Thực thu")
    # Trạng liên hệ
    contact_status = fields.Selection(
        [('notcall', 'Chưa gọi'), ('called', 'Đã gọi')], string='Trạng thái liên hệ')
    # Ghi chú
    notes = fields.Text(string="Ghi chú")
    # Ngày cập nhật cuối ~ __last_update

    # Người cập nhật
    last_update_user = fields.Many2one(
        "res.partner", string="Người cập nhật cuối")
    # Danh sách hành trình
    segment_list = fields.One2many(
        'ticketing.booking.segment', 'booking_id', string='Hành trình')
    # Danh sách hành khách
    passenger_list = fields.One2many(
        'ticketing.booking.passenger', 'booking_id', string='Hành khách')
    # Dịch vụ cộng thêm
    addon_list = fields.One2many(
        'ticketing.booking.addon', 'booking_id', string='Dịch vụ cộng thêm')
    # Danh sách giá
    price_list = fields.One2many(
        'ticketing.booking.price', 'booking_id', string='Danh sách giá')

    @api.onchange('price_list')
    def set_total_price(self):
        print('price_list change')
        self.total_price_amount = 0
        for rec in self.price_list:
            self.total_price_amount += rec.price_after

    @api.onchange('contact_id')
    def contact_select(self):
        self.contact_name = self.contact_id.name
        # Địa chỉ liên lạc
        self.contact_address = self.contact_id.street
        # Số điện thoại
        self.contact_phone = self.contact_id.phone
        # Email liên hệ
        self.contact_email = self.contact_id.email
