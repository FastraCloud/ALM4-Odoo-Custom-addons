# -*- coding: utf-8 -*-
from odoo import http

# class Alm-multi-location(http.Controller):
#     @http.route('/alm-multi-location/alm-multi-location/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/alm-multi-location/alm-multi-location/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('alm-multi-location.listing', {
#             'root': '/alm-multi-location/alm-multi-location',
#             'objects': http.request.env['alm-multi-location.alm-multi-location'].search([]),
#         })

#     @http.route('/alm-multi-location/alm-multi-location/objects/<model("alm-multi-location.alm-multi-location"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('alm-multi-location.object', {
#             'object': obj
#         })