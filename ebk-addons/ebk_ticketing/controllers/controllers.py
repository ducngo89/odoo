# -*- coding: utf-8 -*-
from odoo import http
import json


class Transport(http.Controller):
    @http.route('/transport', auth='public', website=True)
    def index(self, **kw):

        # get location of transport
        locations = http.request.env['ticketing.master.location'].search([])
        # for p in locations:
        #     print(p.location)
        # end get location of transport

        return http.request.render('ebk_ticketing.index', {
            'locations': locations,
        })

    @http.route('/transport/search', auth='public', website=True)
    def list(self, rdbSearchType, txtFromCity, txtToCity, txtDepartureDate, txtReturnDate, dllAdult, dllChild, dllInfant, dllOlder, **kw):
        ships = http.request.env['product.template'].search(
            ['&', ('location_departure', '=', int(txtFromCity)), ('location_arrival', '=', int(txtToCity))])
        print('==================================' +
              txtFromCity + "-" + txtToCity)
        for ship in ships:
            print('---------------------------------')
            print(ship)
        return http.request.render('ebk_ticketing.search', {
            'teachers': ["Diana Padilla", "Jody Caroll", "Lester Vaughn"],
        })
