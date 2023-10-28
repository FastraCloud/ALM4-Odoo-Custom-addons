
# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

class HRExtend(models.Model):
    _inherit = 'hr.employee'

    employee_type = fields.Selection([
           ('expatriate','Expatriate'),
           ('local','Local Staff'),
           ('contract','Contract Staff')
         ],default='local')
    analytic_account = fields.Many2one('account.analytic.account',string="Analytic Account")
    pay_per_hour = fields.Float(string="Amount Paid per hour")
    pay_per_month = fields.Float(string="Amount paid per month")
    pass_isuue_date = fields.Date(string="Passport Issuance Date")
    pass_expiry_date = fields.Date(string="Passport Expiration Date")
    greencard_isuue_date = fields.Date(string="Green Card Issuance Date")
    greencard_expiry_date = fields.Date(string="Green Card Expiry Date")
    join_date = fields.Date(string="Join Date")
    home_country_addr = fields.Char(string="Home Country Address")
    currency_id = fields.Many2one('res.currency', string='Currency')
    timesheet_cost = fields.Monetary('Timesheet Cost', currency_field='currency_id')
    wage = fields.Float()



 #   def name_get(self):
  #      result = []
   #     for record in self:
    #        if record.employee_number:
     #           result.append((record.id, record.employee_number))
      #      else:
       #         result.append((record.id, record.name))
        #return result

class Hr_payslipExtend(models.Model):
    _inherit = "hr.attendance"

    total_hours_worked = fields.Float('Total Hours Worked', store=True)

    @api.multi
    @api.onchange('check_out')
    def compute_total_worked_hours(self):
        time_object_1 = datetime.strptime(str(self.check_in[11:]), '%H:%M:%S').time()
        time_object_2 = datetime.strptime(str(self.check_out[11:]), '%H:%M:%S').time()
#	print(str(self.check_in[11:]), str(self.check_out[11:]))
        date = datetime.strptime('01-01-2000', '%m-%d-%Y').date()
        datetime1 = datetime.combine(date, time_object_1)
        datetime2 = datetime.combine(date, time_object_2)
        time_elapsed = datetime2 - datetime1
#	print(time_elapsed, datetime1, datetime2)
        hours = time_elapsed.seconds//3600
	for rec in self:
	    rec.total_hours_worked = float(hours)
	    #rec.write({'total_hours_worked':hours})
#	print("Hours = ", hours)
#	print(time_elapsed.seconds)


class Hr_payslipExtend(models.Model):
    _inherit = "hr.payslip"
    
    @api.onchange('struct_id')
    def compute_input_lines(self):
        for rec in self:                                                                                                            
            input_lines = []                                                                                                        
            if rec.struct_id:                                                                                                         
                for rule in rec.struct_id.rule_ids:                                                                                       
                    for input in rule.input_ids:                                                                            
                        input_lines.append((0,0,
                            {
                           'name':input.name,
                           'code':input.code, 
                           'contract_id':rec.contract_id.id if rec.contract_id else None
	         	    }))
            rec.input_line_ids = input_lines    



class WageReportCustom(models.Model):
    _name = 'hr.wage.report'
    
    name = fields.Char(string="Reference",default="Wage Report")
    date = fields.Date(string='Date', default=datetime.today())
    prepared_by = fields.Many2one('res.users',string="Prepared By",default=lambda self: self.env.user.id)
    approved_by = fields.Many2one('res.users',string="Äpproved By")
    hr_wage_line = fields.One2many('hr.wage.report.line','hr_wage_id',string="HR Wage Lines")
    start_date = fields.Date(string='Start Date', default=datetime.today())
    end_date = fields.Date(string='End Date', default=datetime.today())
    total = fields.Float(store=True)
    state = fields.Selection([('draft','Draft'),('pending','Awaiting Approval'),('approved','Wage Approved'),('rejected','Wage rejected')],default="draft")

    @api.multi
    @api.onchange('hr_wage_line')
    def onchange_wage_line(self):
        for rec in self.hr_wage_line:
            attendance = self.env['hr.attendance'].search([('employee_id', '=', rec.employee.id)])
            over_time = []
            work_time = []
            start = self.start_date
            stop = self.end_date

            d1 = datetime.strptime(str(start), "%Y-%m-%d")
            d2 = datetime.strptime(str(stop), "%Y-%m-%d")
            days = (d2 - d1).days

            for i in attendance:
                time_object_1 = datetime.strptime(i.check_in[11:], '%H:%M:%S').time()
                time_object_2 = datetime.strptime(i.check_out[11:], '%H:%M:%S').time()

                date1 = datetime.strptime(i.check_in[:10], "%Y-%m-%d")
                date2 = datetime.strptime(i.check_out[:10], "%Y-%m-%d")

                if days > 0:
                    if (d1 - date1).days < days:

                        date = datetime.strptime('01-01-2000', '%m-%d-%Y').date()

                        datetime1 = datetime.combine(date, time_object_1)
                        datetime2 = datetime.combine(date, time_object_2)

                        time_elapsed = datetime2 - datetime1
                        hours = time_elapsed.seconds // 3600
                        time = hours - 9
                        if time > 0:
                            if time > 9:
                                over_time.append(time)
                                work_time.append(9)
                            else:
                                pass
                        else:
                            work_time.append(hours)
            rec.hours_worked = sum(work_time)
            rec.overtime = sum(over_time)
            rec.wage = rec.employee.pay_per_hour
            rec.total_wage = rec.employee.pay_per_hour * sum(work_time)
            rec.total_overtime = rec.employee.pay_per_hour * sum(over_time)
            rec.analytic_account = rec.employee.analytic_account.id
            rec.total = rec.total_overtime + rec.total_wage


    @api.multi
    def send_for_approval(self):
        for rec in self:
            rec.write({'state':'pending'})

    @api.multi
    def approve(self):
        for rec in self:
            rec.write({'state':'approved','approved_by':self.env.user.id})

    @api.multi
    def reject(self):
        for rec in self:
            rec.write({'state':'reject'})



class WageReportCustomLine(models.Model):
    _name = 'hr.wage.report.line'

    hr_wage_id = fields.Many2one('hr.wage.report',string="Hr Wage Report")
    employee = fields.Many2one('hr.employee',string="Employee")
    analytic_account = fields.Many2one('account.analytic.account',string="Analytic Account")
    hours_worked = fields.Integer(string="Hours Worked")
    wage = fields.Float(store=True)
    worked_hours_id = fields.Many2one('hr.attendance', string="Worked Hours", store=True)
    overtime = fields.Float(store=True)
    employee_name = fields.Char(string="Employee Name", store=True)
    total = fields.Float(store=True)
    total_wage = fields.Float(store=True)
    total_overtime = fields.Float(store=True)

    @api.multi
    @api.onchange('employee')
    def onchange_compute_location(self):
       # print("=======================================")
       # print(self.employee.pay_per_hour)
        attendance = self.env['hr.attendance'].search([('employee_id', '=', self.employee.id)])
	over_time = []
	work_time = []
	start = self.hr_wage_id.start_date
	stop = self.hr_wage_id.end_date

	d1 = datetime.strptime(str(start), "%Y-%m-%d")
    	d2 = datetime.strptime(str(stop), "%Y-%m-%d")
	days = (d2 - d1).days

	for i in attendance:
            time_object_1 = datetime.strptime(i.check_in[11:], '%H:%M:%S').time()
            time_object_2 = datetime.strptime(i.check_out[11:], '%H:%M:%S').time()

	    date1 = datetime.strptime(i.check_in[:10], "%Y-%m-%d")
	    date2 = datetime.strptime(i.check_out[:10], "%Y-%m-%d")

	    if days > 0:
                if (d1 - date1).days < days:

                    date = datetime.strptime('01-01-2000', '%m-%d-%Y').date()

                    datetime1 = datetime.combine(date, time_object_1)
                    datetime2 = datetime.combine(date, time_object_2)

                    time_elapsed = datetime2 - datetime1
                    hours = time_elapsed.seconds // 3600
                    # work_time.append(hours)
                    time = hours - 9
                    if time > 0:
                        if time > 9:
                            over_time.append(time)
                            work_time.append(9)
                        else:
                            pass
                    else:
                        work_time.append(hours)

	#print(over_time, "    ", work_time)
	self.hours_worked = float(sum(work_time))
	self.overtime = float(sum(over_time))
	self.wage = self.employee.pay_per_hour
	self.total_wage = float(self.employee.pay_per_hour * sum(work_time))
	self.total_overtime = float(self.employee.pay_per_hour * sum(over_time))
	self.analytic_account = self.employee.analytic_account.id
	self.total = float(self.total_overtime + self.total_wage)
	print(self.employee.pay_per_hour)
        #for rec in self:
         #   if rec.employee:
               # rec.analytic_account = rec.employee.analytic_account.id
                #rec.wage = rec.employee.wage
                #rec.employee_name = rec.employee.name
		#rec.worked_hours_id = rec.worked_hours_id.worked_hours
                #rec.hours_worked = sum(work_time)
        	#rec.overtime = sum(over_time)
        	#rec.wage = self.employee.pay_per_hour
        	#rec.total_wage = self.employee.pay_per_hour * sum(work_time)
        	#rec.total_overtime = self.employee.pay_per_hour * sum(over_time)
        	#rec.analytic_account = self.employee.analytic_account.id
        	#rec.total = self.total_overtime + self.total_wage


    #@api.onchange('wage','overtime')
    #def onchange_compute_total(self):
        #self.total = self.wage + (self.overtime*self.employee.pay_per_hour)
	#self.total = self.total_overtime + self.total_wage


class Hr_ticketing(models.Model):
    _name = 'hr.ticketing'


    employee = fields.Many2one('res.users',string="Employee",default=lambda self: self.env.user.id)
    destination = fields.Text()
    state = fields.Selection([('draft','Draft'),('pending','Awaiting Approval'),('approved','Approved and Booked'),('rejected','Rejected')],default='draft')

    @api.multi
    def send_for_approval(self):
        for rec in self:
            rec.write({'state':'pending'})


    @api.multi
    def approve(self):
        for rec in self:
            rec.write({'state':'approved'})

    @api.multi
    def reject(self):
        for rec in self:
            rec.write({'state':'rejected'})









    #@api.model
    #def create(self, vals):
    #     if vals['wage'] and vals['overtime']:
    #         vals['total'] = vals['wage'] + vals['overtime']
    #     res = super(WageReportCustomLine, self).create(vals)        
    #     return res

    #@api.multi
    #def write(self, vals):
     #   print(vals)
     #   if 'wage' in vals or 'overtime' in vals:
     #       vals['total'] = vals['wage'] + vals['overtime']
     #   res = super(WageReportCustomLine, self).write(vals)
     #   return res
