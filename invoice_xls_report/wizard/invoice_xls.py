# -*- coding: utf-8 -*-
import xlwt
import base64
import calendar
from io import StringIO
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, Warning
from datetime import datetime

class InvoiceReport(models.TransientModel):
    _name = "invoice.report"
    
    start_date = fields.Date(string='Start Date', required=True, default=datetime.today().replace(day=1))
    end_date = fields.Date(string="End Date", required=True, default=datetime.now().replace(day = calendar.monthrange(datetime.now().year, datetime.now().month)[1]))
    invoice_state = fields.Selection([
            ('open', 'Open'),
            ('paid', 'Paid'),
        ], string='Status', default='open', required=True)
    partner_select = fields.Selection([
            ('customer','Customer'),
            ('vendor', 'Vendor'),
            ('both', 'Both'),
        ], string='Partner', default='customer', required=True)
    invoice_data = fields.Char('Name',)
    file_name = fields.Binary('Invoice Excel Report', readonly=True)
    state = fields.Selection([('choose', 'choose'), ('get', 'get')],
                             default='choose')

    _sql_constraints = [
            ('check','CHECK((start_date <= end_date))',"End date must be greater then start date")  
    ]

    @api.multi
    def action_invoice_report(self):
        invoice = self.env['account.invoice'].search([('date_invoice', '>=', self.start_date), ('date_invoice', '<=', self.end_date), 
                                                    ('state', '=', self.invoice_state)])
        record = []
        if invoice:
            for rec in invoice:
                if self.partner_select == "customer" and rec.partner_id.customer == True and rec.partner_id.supplier == False:
                    record.append(rec)
                elif self.partner_select == "vendor" and rec.partner_id.supplier == True and rec.partner_id.customer == False:
                    record.append(rec)
                elif self.partner_select == "both" and rec.partner_id.customer == True and rec.partner_id.supplier == True:
                    record.append(rec)
            file = StringIO()        
            final_value = {}
            workbook = xlwt.Workbook()                         
            if record:
                for rec in record:
                    invoice_lines = []
                    for lines in rec.invoice_line_ids:
                        product = {
                            'product_id'     : lines.product_id.name,
                            'description'    : lines.name,
                            'quantity'       : lines.quantity,
                            'price_unit'     : lines.price_unit,
                            'price_subtotal' : lines.price_subtotal   
                        }
                        if lines.invoice_line_tax_ids:
                            taxes = []
                            for tax_id in lines.invoice_line_tax_ids:
                                taxes.append(tax_id.name)
                            product['invoice_line_tax_ids'] = taxes
                        invoice_lines.append(product)
                    final_value['partner_id'] = rec.partner_id.name
                    final_value['date_invoice'] = rec.date_invoice
                    final_value['date_due'] = rec.date_due
                    final_value['number'] = rec.number
                    final_value['currency_id'] = rec.currency_id
                    final_value['state'] = dict(self.env['account.invoice'].fields_get(allfields=['state'])['state']['selection'])[rec.state]
                    final_value['payment_term_id'] = rec.payment_term_id.name
                    final_value['origin'] = rec.origin
                    final_value['amount_untaxed'] = rec.amount_untaxed
                    final_value['amount_tax'] = rec.amount_tax
                    final_value['amount_total'] = rec.amount_total
                    final_value['residual'] = rec.residual
                    final_value['payments_widget'] = rec.payments_widget
                    final_value['outstanding_credits_debits_widget'] = rec.outstanding_credits_debits_widget                
                    format0 = xlwt.easyxf('font:height 500,bold True;pattern: pattern solid, fore_colour gray25;align: horiz center')
                    format1 = xlwt.easyxf('font:bold True;pattern: pattern solid, fore_colour gray25;align: horiz left')
                    format2 = xlwt.easyxf('font:bold True;align: horiz left')
                    format3 = xlwt.easyxf('align: horiz left')
                    format4 = xlwt.easyxf('align: horiz right')
                    format5 = xlwt.easyxf('font:bold True;align: horiz right')
                    format6 = xlwt.easyxf('font:bold True;pattern: pattern solid, fore_colour gray25;align: horiz right')
                    format7 = xlwt.easyxf('font:bold True;borders:top thick;align: horiz right')
                    format8 = xlwt.easyxf('font:bold True;borders:top thick;pattern: pattern solid, fore_colour gray25;align: horiz left')
                    invoice_number = rec.number.split('/')
                    sheet = workbook.add_sheet(invoice_number[0]+'-'+invoice_number[1]+'-'+invoice_number[2])
                    sheet.col(0).width = int(30*260)
                    sheet.col(1).width = int(30*260)    
                    sheet.col(2).width = int(18*260)    
                    sheet.col(3).width = int(18*260) 
                    sheet.col(4).width = int(33*260)   
                    sheet.col(5).width = int(15*260)
                    sheet.col(6).width = int(18*260)   
                    if self.partner_select == "customer":
                        sheet.write_merge(0, 2, 0, 5, 'Customer Invoices : ' + final_value['number'] , format0)
                        sheet.write(5, 0, "Customer", format1)
                        sheet.write(5, 1, final_value['partner_id'], format2)
                        sheet.write(5, 3, 'Invoice Date', format1)
                    elif self.partner_select == "vendor":
                        sheet.write_merge(0, 2, 0, 5, 'Vendor Bills : ' + final_value['number'] , format0)
                        sheet.write(5, 0, "Vendor", format1)
                        sheet.write(5, 1, final_value['partner_id'], format2)
                        sheet.write(5, 3, 'Bill Date', format1)
                    elif self.partner_select == "both":
                        sheet.write_merge(0, 2, 0, 5, 'Invoice : ' + final_value['number'] , format0)
                        sheet.write(5, 0, "Partner", format1)
                        sheet.write(5, 1, final_value['partner_id'], format2)
                        sheet.write(5, 3, 'Date', format1)
                    sheet.write_merge(5, 5, 4, 5, final_value['date_invoice'], format3)
                    sheet.write(6, 3, 'Due Date', format1)
                    sheet.write_merge(6, 6, 4, 5, final_value['date_due'], format3)
                    sheet.write(7, 3, 'Payment Term', format1)
                    if final_value['payment_term_id']:
                        sheet.write_merge(7, 7, 4, 5, final_value['payment_term_id'], format3)
                    else:
                        sheet.write_merge(7, 7, 4, 5, "No Payment Terms Defined", format3)
                    sheet.write(8, 3, "State", format1)
                    sheet.write_merge(8, 8, 4, 5, final_value['state'], format3)
                    sheet.write(10, 0, "Source Document", format1)
                    if final_value['origin']:
                        sheet.write(11, 0, final_value['origin'], format3)
                    else:
                        sheet.write(11, 0, "No Origin", format3)
                    sheet.write(15, 0, 'PRODUCT', format1)
                    sheet.write(15, 1, 'DESCRIPTION', format1)
                    sheet.write(15, 2, 'QUANTITY', format6)                
                    sheet.write(15, 3, 'UNIT PRICE', format6)
                    sheet.write(15, 4, 'TAXES', format1) 
                    sheet.write(15, 5, 'SUBTOTAL', format6)
                    row = 16
                    for rec in invoice_lines:
                        sheet.write(row, 0, rec.get('product_id'), format3)
                        sheet.write(row, 1, rec.get('description'), format3)
                        sheet.write(row, 2, rec.get('quantity'), format4)
                        sheet.write(row, 3, rec.get('price_unit'), format4)
                        if rec.get('invoice_line_tax_ids'):
                            sheet.write(row, 4, ",".join(rec.get('invoice_line_tax_ids')), format4)
                        else:
                            sheet.write(row, 4, "No Taxes", format4)
                        if final_value['currency_id'].position == "before":
                            sheet.write(row, 5, final_value['currency_id'].symbol + str(rec.get('price_subtotal')), format4)
                        else:
                            sheet.write(row, 5, str(rec.get('price_subtotal')) + final_value['currency_id'].symbol, format4)
                        row += 1
                    row += 2
                    sheet.write(row, 4, 'UNTAXED AMOUNT', format8)
                    if final_value['currency_id'].position == "before":
                        sheet.write(row, 5, final_value['currency_id'].symbol + str(final_value['amount_untaxed']), format7)
                    else:
                        sheet.write(row, 5, str(final_value['amount_untaxed']) + final_value['currency_id'].symbol, format7)    
                    sheet.write(row+1, 4, 'TAXES', format8)
                    if final_value['currency_id'].position == "before":
                        sheet.write(row+1, 5, final_value['currency_id'].symbol + str(final_value['amount_tax']), format7)
                    else:
                        sheet.write(row+1, 5, str(final_value['amount_tax']) + final_value['currency_id'].symbol, format7)
                    sheet.write(row+2, 4, 'TOTAL', format8)
                    if final_value['currency_id'].position == "before":
                        sheet.write(row+2, 5, final_value['currency_id'].symbol + str(final_value['amount_total']), format7)
                    else:
                        sheet.write(row+2, 5, str(final_value['amount_total']) + final_value['currency_id'].symbol, format7)
                    sheet.write(row+4, 4, 'AMOUNT DUE', format8)
                    if final_value['currency_id'].position == "before":
                        sheet.write(row+4, 5, final_value['currency_id'].symbol + str(final_value['residual']), format7)
                    else:
                        sheet.write(row+4, 5, str(final_value['residual']) + final_value['currency_id'].symbol, format7)    
            else:
                raise Warning("Currently No Invoice/Bills For This Data!!")
            filename = ('Invoice Report'+ '.xls')
            workbook.save(filename)
            file = open(filename, "rb")
            file_data = file.read()
            out = base64.encodestring(file_data)
            self.write({'state': 'get', 'file_name': out, 'invoice_data':'Invoice Report.xls'})
            return {
               'type': 'ir.actions.act_window',
               'res_model': 'invoice.report',
               'view_mode': 'form',
               'view_type': 'form',
               'res_id': self.id,
               'target': 'new',
            }                      
        else:
            raise Warning("Currently No Invoice/Bills For This Data!!")
