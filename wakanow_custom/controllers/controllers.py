# -*- coding: utf-8 -*-
from odoo import http

# class WakanowCustom(http.Controller):
#     @http.route('/wakanow_custom/wakanow_custom/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/wakanow_custom/wakanow_custom/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('wakanow_custom.listing', {
#             'root': '/wakanow_custom/wakanow_custom',
#             'objects': http.request.env['wakanow_custom.wakanow_custom'].search([]),
#         })

#     @http.route('/wakanow_custom/wakanow_custom/objects/<model("wakanow_custom.wakanow_custom"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('wakanow_custom.object', {
#             'object': obj
#         })