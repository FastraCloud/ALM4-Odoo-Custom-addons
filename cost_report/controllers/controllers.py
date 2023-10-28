# -*- coding: utf-8 -*-
from odoo import http

# class CostReport(http.Controller):
#     @http.route('/cost_report/cost_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cost_report/cost_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cost_report.listing', {
#             'root': '/cost_report/cost_report',
#             'objects': http.request.env['cost_report.cost_report'].search([]),
#         })

#     @http.route('/cost_report/cost_report/objects/<model("cost_report.cost_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cost_report.object', {
#             'object': obj
#         })