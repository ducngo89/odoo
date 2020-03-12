# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

# ducngo
# 16DEC19


class BookingPassenger(models.Model):
    _name = 'ticketing.booking.passenger'
    _rec_name = 'fullname'
    # Mã booking
    booking_id = fields.Many2one('ticketing.booking', string='Booking ID')
    # Loại hành khách
    pax_type = fields.Selection(
        [('adt', 'Người lớn'), ('chd', 'Trẻ em'), ('inf', 'Sơ sinh')], string='Loại hành khách', required=True)
    # Tên khách hàng
    last_name = fields.Char(string='Tên đệm & tên', required=True)
    # Họ khách hàng
    first_name = fields.Char(string='Họ hành khách', required=True)
    # Ngày sinh
    dob = fields.Date(string='Ngày sinh', required=True)
    # Giớ tính
    sex = fields.Selection(
        [('male', 'Nam'), ('female', 'Nữ')], string='Giới tính', required=True)
    # CMND/Hộ chiếu
    pax_no = fields.Char(string='CMND/Hộ chiếu')
    # Ngày cấp
    issue_date = fields.Date(string='Ngày cấp')
    # Nơi cấp
    issue_country_state_id = fields.Many2one('res.country.state')
    # Quốc gia
    issue_country_id = fields.Many2one('res.country')

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

    # Số vé chiều đi
    ticket_no_departure = fields.Char(string='Số vé chiều đi')
    # Số vé chiều về
    ticket_no_return = fields.Char(string='Số vé chiều về')
    # Số hóa đơn
    vat_no = fields.Char(string='Số hóa đơn')
    # Ghi chú
    notes = fields.Char(string='Ghi chú')

    fullname = fields.Char(string="Họ & tên", compute='_combine_name')

    def _combine_name(self):
        for rec in self:
            if rec and rec.first_name and rec.last_name:
                rec.fullname = rec.first_name + '/' + rec.last_name

    passenger_id = fields.Many2one(
        'ticketing.passenger', string='Tìm hành khách')

    @api.onchange('passenger_id')
    def on_passenger_select(self):
        self.last_name = self.passenger_id.last_name
        self.first_name = self.passenger_id.first_name
        self.dob = self.passenger_id.dob
        self.sex = self.passenger_id.sex

        self.phone = self.passenger_id.phone
        self.mobile = self.passenger_id.mobile
        self.email = self.passenger_id.email


        self.pax_no = self.passenger_id.pax_no
        self.issue_date = self.passenger_id.issue_date
        self.issue_country_state_id = self.passenger_id.issue_country_state_id
        self.issue_country_id = self.passenger_id.issue_country_id
        #self.fullname = self.passenger_id.first_name + '/' + self.passenger_id.last_name

        self.passport_no = self.passenger_id.passport_no
        self.passport_issue_date = self.passenger_id.passport_issue_date
        self.passport_due_date = self.passenger_id.passport_due_date
        self.passport_issue_country_state_id = self.passenger_id.passport_issue_country_state_id
        self.passport_issue_country_id = self.passenger_id.passport_issue_country_id
