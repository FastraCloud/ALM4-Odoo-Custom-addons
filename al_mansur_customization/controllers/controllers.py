# -*- coding: utf-8 -*-
from odoo import http

# class AlMansurCustomization(http.Controller):
#     @http.route('/al_mansur_customization/al_mansur_customization/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/al_mansur_customization/al_mansur_customization/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('al_mansur_customization.listing', {
#             'root': '/al_mansur_customization/al_mansur_customization',
#             'objects': http.request.env['al_mansur_customization.al_mansur_customization'].search([]),
#         })

#     @http.route('/al_mansur_customization/al_mansur_customization/objects/<model("al_mansur_customization.al_mansur_customization"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('al_mansur_customization.object', {
#             'object': obj
#         })