# -*- coding: utf-8 -*-

from odoo import models, fields, api
from dateutil.relativedelta import *
from datetime import date


class ProductInherit(models.Model):
    _inherit = 'product.template'
    rental_ok = fields.Boolean(string='Can be Rental')

    @api.onchange('type')
    def _onchange_type_for_expense(self):
        # storable can not be expensed.
        if self.type not in ['service']:
            self.rental_ok = False


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def action_confirm(self):
        super(SaleOrder, self).action_confirm()
        # do something
        if self.order_line:
            # get customer service
            service = self.env['rental.customerservice'].search(
                [('partner_id', '=', self.partner_id.id)])
            # end get customer service
            for rec in self.order_line:

                if rec.product_id.rental_ok:

                    # create customer service if not exists
                    if not service:
                        vals = {
                            "partner_id": self.partner_id.id,
                            "start_date": self.create_date,
                        }
                        service = self.env['rental.customerservice'].create(
                            vals)
                        print('Create customer service', self.partner_id)
                    # end create customer service if not exists

                    # create service line

                    service_line = self.env['rental.service.lines'].search(
                        ['&', ('customer_service_id', '=', service.id), ('product_id', '=', rec.product_id.id)])
                    if not service_line:
                        # create service line if not exists
                        vals = {
                            "customer_service_id": service.id,
                            "product_id": rec.product_id.id,
                            "start_date": self.date_order,
                            "expried_date": self.date_order + relativedelta(months=+int(rec.product_uom_qty))
                        }
                        self.env['rental.service.lines'].create(
                            vals)
                        print('Create service line', rec.product_id.id)
                        # end create service line if not exists
                    else:
                        # update expried_date if service line exists
                        print('rec.product_uom', rec.product_uom.name)
                        if rec.product_uom.name == 'Month':
                            service_line.expried_date = service_line.expried_date + \
                                relativedelta(
                                    months=+int(rec.product_uom_qty))

                        if rec.product_uom.name == 'Year':
                            service_line.expried_date = service_line.expried_date + \
                                relativedelta(
                                    years=+int(rec.product_uom_qty))
            if service:
                # create order line
                vals = {
                    "customer_service_id": service.id,
                    "order_id": self.id,
                    "amount_total": self.amount_total,
                    "date_order": self.date_order,
                }
                self.env['rental.order.lines'].create(
                    vals)
                print('Create order line', self.partner_id)
                # end create order line

                # compute time exp
                service.compute_expried_date()
                # end compute time exp

                # post message
                service.message_post(
                    body=self.create_uid.name + " Tạo hóa đơn: " + self.name, subject="Tạo mới hóa đơn")
                # end post message

                # add revenue by month
                service_lines = self.env['rental.service.lines'].search(
                    [('customer_service_id', '=', service.id)])
                for service in service_lines:
                    total_money = 0
                    months = 0
                    for line in self.order_line:
                        if line.product_id.rental_ok == True and line.product_id.id == service.product_id.id:
                            total_money += line.price_subtotal
                            if line.product_uom.name == 'Year':
                                months += line.product_uom_qty*12
                            else:
                                months += line.product_uom_qty
                            avg_money = total_money/months
                    # create registerservice
                    for i in range(int(months)):
                        vals = {
                            "partner_id": self.partner_id.id,
                            "product_id": service.product_id.id,
                            "order_id": self.id,
                            "register_date": service.expried_date+relativedelta(months=-i-1),
                            "month_report": (service.expried_date+relativedelta(months=-i-1)).strftime("%Y-%m"),
                            "money": avg_money,
                        }
                        self.env['rental.registerservice'].create(
                            vals)
                    # end create registerservice

                # end add revenue by month
        return True

    @api.model
    def action_cancel(self):
        super(SaleOrder, self).action_cancel()
        service = self.env['rental.customerservice'].search(
            [('partner_id', '=', self.partner_id.id)])
        if service:
            # delete order line
            customer_order_line = self.env['rental.order.lines'].search(
                [('order_id', '=', self.id)], limit=1)
            if customer_order_line:
                customer_order_line.unlink()
                service.message_post(
                    body=self.create_uid.name + " Hủy hóa đơn: " + self.name, subject="Hủy hóa đơn")
            # end delete order line

            # delete register service line
            service_line = self.env['rental.registerservice'].search(
                [('order_id', '=', self.id)])
            if service_line:
                for rec in service_line:
                    rec.unlink()
            # end delete register service line

            if self.order_line:
                # end get customer service
                for rec in self.order_line:
                    service_line = self.env['rental.service.lines'].search(
                        ['&', ('customer_service_id', '=', service.id), ('product_id', '=', rec.product_id.id)])
                    if service_line:
                        if rec.product_uom.name == 'Month':
                            if service_line.expried_date > self.date_order.date():
                                service_line.expried_date = service_line.expried_date - \
                                    relativedelta(
                                        months=+int(rec.product_uom_qty))
                            else:
                                service_line.expried_date = self.date_order.date() - \
                                    relativedelta(
                                        months=+int(rec.product_uom_qty))
                        if rec.product_uom.name == 'Year':
                            if service_line.expried_date > self.date_order.date():
                                service_line.expried_date = service_line.expried_date - \
                                    relativedelta(
                                        years=+int(rec.product_uom_qty))
                            else:
                                service_line.expried_date = self.date_order.date() - \
                                    relativedelta(
                                        years=+int(rec.product_uom_qty))
            # compute time exp
            service.compute_expried_date()
            # end compute time exp

        return True


class RegisterServices(models.Model):
    _name = 'rental.registerservice'
    _description = 'Register Service Record'
    _order = "id desc"

    partner_id = fields.Many2one('res.partner', string="Khách hàng")
    product_id = fields.Many2one('product.template', string="Dịch vụ")
    order_id = fields.Many2one('sale.order', string="Mã đơn hàng")
    register_date = fields.Date(string="Ngày thanh toán")
    money = fields.Float(string="Số tiền")

    month_report = fields.Char(
        string="Tháng báo cáo", compute="_compute_month", store=True)

    @api.depends('register_date')
    def _compute_month(self):
        for rec in self:
            if rec.register_date is not None:
                rec.month_report = rec.register_date.strftime("%Y-%m")
