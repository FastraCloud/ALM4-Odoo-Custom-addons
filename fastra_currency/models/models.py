# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class fastra_currency(models.Model):
#     _name = 'fastra_currency.fastra_currency'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100

class UpdateCurrency(models.Model):
    _inherit = 'account.invoice'

    
    @api.multi
    @api.onchange('state')
    def get_right_currency(self):
        for rec in self:
            data = rec.move_id
            print(data)
            for i in data.line_ids:
                if i.currency_id != i.company_currency_id:
                    currency_data = self.env['account.move'].search([('id', '=', i.id)], limit=1)
                    currency_value = self.env['res.currency'].search([('id', '=', i.currency_id)], limit=1)
                    rate = currency_value.rate
                    print(currency_data, currency_value, rate)
                    print('----------------------------------------------------------------------------------')
                    # currency_data.write({''})
                    
            
            
