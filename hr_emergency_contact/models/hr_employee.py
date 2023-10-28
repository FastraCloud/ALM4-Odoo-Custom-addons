# -*- coding: utf-8 -*-
# copyright 2011 Michael Telahun Makonnen <mmakonnen@gmail.com>
# copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class HrEmployee(models.Model):

    _inherit = 'hr.employee'
    emergency_contact_ids_new = fields.One2many('hr.emergency.contact', 'related_staff',
			    string='Emergency Contacts')


class EmployeeEmergency(models.Model):
    _name = 'hr.emergency.contact'
    
    name = fields.Char('Name')
    mobile_number = fields.Char('Mobile Number')
    email = fields.Char('Email')
    address_id = fields.Char('Home Address')
    relationship = fields.Char('Relationship')
    related_staff = fields.Many2one('hr.employee', 'Related Employee')



class HrEmployee(models.Model):

    _inherit = 'hr.employee'

    emergency_contact_ids = fields.Many2one( comodel_name='res.partner',
	string='Emergency Contacts',
	relation='rel_employee_emergency_contact',
	domain=[('is_company', '=', False)]
	)
