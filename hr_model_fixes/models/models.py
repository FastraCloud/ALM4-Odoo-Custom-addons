# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

# class hr_model_fixes(models.Model):
#     _name = 'hr_model_fixes.hr_model_fixes'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100


class Employee(models.Model):
    _inherit = "hr.employee"

    #newly added fields
    green_card_issue = fields.Date('Green Card Issue Date')
    green_card_expiry = fields.Date('Green Card Expiry Date')
    passport_issue = fields.Date('Passport Issue Date')
    passport_expiry = fields.Date('Passport Expiry Date')
    home_country_add = fields.Text('Home Country Address')
    home_country_emergency_contact = fields.Char('Emergency Contact in home country')
    
