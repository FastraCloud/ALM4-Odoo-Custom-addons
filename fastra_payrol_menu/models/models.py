
from odoo import models, fields, api
import datetime

class Payslip_Extension(models.Model):
    _inherit = 'hr.payslip'

    workdays = fields.Integer('Workdays', compute="_compute_workdays")


    @api.onchange('date_from', 'date_to')
    def _compute_workdays(self):
        self.ensure_one()
        
        date_unicode = self.date_from

        now = datetime.datetime.strptime(date_unicode, '%Y-%m-%d')


        holidays = {datetime.date(now.year, 1, 3), datetime.date(now.year, 4, 15), datetime.date(now.year, 4, 18), datetime.date(now.year, 5, 2), datetime.date(now.year, 5, 3), datetime.date(now.year, 5, 4),
        datetime.date(now.year, 6, 13), datetime.date(now.year, 7, 11), datetime.date(now.year, 10, 3), datetime.date(now.year, 10, 8),
        datetime.date(now.year, 12, 26), datetime.date(now.year, 12, 27)} # you can add more here
        businessdays = 0
        for i in range(1, 32):
            try:
                thisdate = datetime.date(now.year, now.month, i)
            except(ValueError):
                break
            if thisdate.weekday() < 5 and thisdate not in holidays: # Monday == 0, Sunday == 6 
                businessdays += 1

        self.workdays = businessdays

    

                