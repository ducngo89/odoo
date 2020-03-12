# -*- coding: utf-8 -*-

from odoo import models, fields, api
from dateutil.relativedelta import *
from datetime import date


class CustomerServices(models.Model):
    _name = 'rental.customerservice'
    _description = 'Customer Service Record'
    _inherit = ['mail.thread.cc', 'mail.activity.mixin']
    _rec_name = "website"
    _order="expried_date"

    partner_id = fields.Many2one(
        'res.partner', string="Khách hàng", required=True)
    website = fields.Char(string="Website", related="partner_id.website")
    start_date = fields.Date(string="Ngày bắt đầu", required=True)
    expried_date = fields.Date(string="Ngày hết hạn")
    service_lines = fields.One2many(
        'rental.service.lines', 'customer_service_id', string="Dịch vụ đăng ký")

    order_lines = fields.One2many(
        'rental.order.lines', 'customer_service_id', string="Đơn hàng đã lập")

    notes = fields.Text(string="Ghi chú")

    status = fields.Selection([('expired', 'Đã hết hạn'), ('on_time',
                                                           'Sắp hết hạn'), ('going', 'Còn hạn')],
                              string="Trạng thái", compute="compute_status", store=True)

    def update_status(self):
        customerservice = self.search([])
        for rec in customerservice:
            if rec.expried_date:
                date5 = date.today()+relativedelta(days=+5)

                if rec.expried_date < date.today():
                    rec.status = 'expired'
                else:
                    if rec.expried_date <= date5:
                        rec.status = 'on_time'
                    else:
                        rec.status = 'going'

    @api.onchange("service_lines")
    def compute_expried_date(self):
        print('cumpute_expried_date')
        if self.service_lines:
            self.expried_date = min(i.expried_date
                                    for i in self.service_lines)
        else:
            self.expried_date = None
        date5 = date.today()+relativedelta(days=+5)

        if self.expried_date < date.today():
            self.status = 'expired'
        else:
            if self.expried_date <= date5:
                self.status = 'on_time'
            else:
                self.status = 'going'

    @api.depends('expried_date')
    def compute_status(self):
        print('compute_status')
        for rec in self:
            if rec.expried_date:
                date5 = date.today()+relativedelta(days=+5)

                if rec.expried_date < date.today():
                    rec.status = 'expired'
                else:
                    if rec.expried_date <= date5:
                        rec.status = 'on_time'
                    else:
                        rec.status = 'going'


class ServiceLine(models.Model):
    _name = "rental.service.lines"
    customer_service_id = fields.Many2one(
        'rental.customerservice', string="Khách hàng")
    product_id = fields.Many2one('product.template', string="Dịch vụ", domain=[
        ('rental_ok', '=', True)])
    start_date = fields.Date(string="Ngày bắt đầu")
    expried_date = fields.Date(string="Ngày hết hạn")
    notes = fields.Text(string="Ghi chú")


class OrderLines(models.Model):
    _name = "rental.order.lines"
    customer_service_id = fields.Many2one(
        'rental.customerservice', string="Khách hàng")
    order_id = fields.Many2one("sale.order", string="Đơn hàng")
    amount_total = fields.Float(
        string="Tổng tiền")
    date_order = fields.Datetime(string="Ngày đơn hàng")
