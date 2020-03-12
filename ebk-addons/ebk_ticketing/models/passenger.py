# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

# ducngo
# 16DEC19


class BookingPassenger(models.Model):
    _name = 'ticketing.passenger'
    _rec_name = 'fullname'
    _inherit = ['mail.thread.cc', 'mail.activity.mixin']

    image = fields.Image(string="Hình đại diện")
    # Tên khách hàng
    last_name = fields.Char(string='Tên đệm & tên')
    # Họ khách hàng
    first_name = fields.Char(string='Họ hành khách')
    # Ngày sinh
    dob = fields.Date(string='Ngày sinh')
    # Giớ tính
    sex = fields.Selection(
        [('male', 'Nam'), ('female', 'Nữ')], string='Giới tính')
    # CMND/Hộ chiếu
    pax_no = fields.Char(string='CMND')
    # Ngày cấp
    issue_date = fields.Date(string='Ngày cấp')
    # Nơi cấp
    issue_country_state_id = fields.Many2one(
        'res.country.state', string=_("Nơi cấp"))
    # Quốc gia
    issue_country_id = fields.Many2one('res.country', string=_("Quốc gia"))

    # Hộ chiếu
    passport_no = fields.Char(string='Passport')
    # Ngày cấp
    passport_issue_date = fields.Date(string='Ngày cấp')
    # Ngày cấp
    passport_due_date = fields.Date(string='Ngày hết hạn')
    # Nơi cấp
    passport_issue_country_state_id = fields.Many2one(
        'res.country.state', string=_("Nơi cấp"))
    # Quốc gia
    passport_issue_country_id = fields.Many2one(
        'res.country', string=_("Quốc gia"))

    phone = fields.Char(string=_("Điện thoại"))
    mobile = fields.Char(string=_("Di động"))
    email = fields.Char(string=_("Email"))

    # Địa chỉ
    street = fields.Char(string=_("Địa chỉ"))

    state_id = fields.Many2one('res.country.state')
    country_id = fields.Many2one('res.country')
    # Ghi chú
    notes = fields.Char(string='Ghi chú')

    fullname = fields.Char(string="Họ & tên", compute='_combine_name')

    def _combine_name(self):
        for rec in self:
            rec.fullname = rec.first_name + '/' + rec.last_name
