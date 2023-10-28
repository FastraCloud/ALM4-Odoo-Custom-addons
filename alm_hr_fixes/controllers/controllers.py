# -*- coding: utf-8 -*-
from odoo import http

# class AlmHrFixes(http.Controller):
#     @http.route('/alm_hr_fixes/alm_hr_fixes/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/alm_hr_fixes/alm_hr_fixes/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('alm_hr_fixes.listing', {
#             'root': '/alm_hr_fixes/alm_hr_fixes',
#             'objects': http.request.env['alm_hr_fixes.alm_hr_fixes'].search([]),
#         })

#     @http.route('/alm_hr_fixes/alm_hr_fixes/objects/<model("alm_hr_fixes.alm_hr_fixes"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('alm_hr_fixes.object', {
#             'object': obj
#         })