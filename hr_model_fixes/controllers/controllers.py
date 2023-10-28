# -*- coding: utf-8 -*-
from odoo import http

# class HrModelFixes(http.Controller):
#     @http.route('/hr_model_fixes/hr_model_fixes/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hr_model_fixes/hr_model_fixes/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hr_model_fixes.listing', {
#             'root': '/hr_model_fixes/hr_model_fixes',
#             'objects': http.request.env['hr_model_fixes.hr_model_fixes'].search([]),
#         })

#     @http.route('/hr_model_fixes/hr_model_fixes/objects/<model("hr_model_fixes.hr_model_fixes"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hr_model_fixes.object', {
#             'object': obj
#         })