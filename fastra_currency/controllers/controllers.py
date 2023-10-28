# -*- coding: utf-8 -*-
from odoo import http

# class FastraCurrency(http.Controller):
#     @http.route('/fastra_currency/fastra_currency/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/fastra_currency/fastra_currency/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('fastra_currency.listing', {
#             'root': '/fastra_currency/fastra_currency',
#             'objects': http.request.env['fastra_currency.fastra_currency'].search([]),
#         })

#     @http.route('/fastra_currency/fastra_currency/objects/<model("fastra_currency.fastra_currency"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('fastra_currency.object', {
#             'object': obj
#         })