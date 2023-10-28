# -*- coding: utf-8 -*-
from odoo import http

# class Alm-report(http.Controller):
#     @http.route('/alm-report/alm-report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/alm-report/alm-report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('alm-report.listing', {
#             'root': '/alm-report/alm-report',
#             'objects': http.request.env['alm-report.alm-report'].search([]),
#         })

#     @http.route('/alm-report/alm-report/objects/<model("alm-report.alm-report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('alm-report.object', {
#             'object': obj
#         })