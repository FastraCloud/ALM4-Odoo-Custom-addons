# -*- coding: utf-8 -*-
from odoo import http

# class FastraPayrolMenu(http.Controller):
#     @http.route('/fastra_payrol_menu/fastra_payrol_menu/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/fastra_payrol_menu/fastra_payrol_menu/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('fastra_payrol_menu.listing', {
#             'root': '/fastra_payrol_menu/fastra_payrol_menu',
#             'objects': http.request.env['fastra_payrol_menu.fastra_payrol_menu'].search([]),
#         })

#     @http.route('/fastra_payrol_menu/fastra_payrol_menu/objects/<model("fastra_payrol_menu.fastra_payrol_menu"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('fastra_payrol_menu.object', {
#             'object': obj
#         })