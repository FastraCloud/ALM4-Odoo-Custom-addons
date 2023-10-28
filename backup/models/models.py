# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError as Warning

# class AlmReport(models.Model):
#     _name = 'alm.report'
#     _description = "For customized accounting reports, sorted by analytic accounts"

#     name = fields.Char('Name', compute="_compute_name", store=True)
#     report_type_ids = fields.Many2many('ir.actions.report.xml')    
#     analytic_acc_ids = fields.Many2many('account.analytic.account', string="Analytic Account(s)")


#     @api.multi
#     def write(self, values):
#         super(AlmReport, self).write(values)
#         if len(self.report_type_ids) > 1:
#             raise Warning('You can only select one(1) Report type')
#         return True


#     @api.depends('analytic_acc_ids', 'report_type_ids')
#     def _compute_name(self):
#         analytics = ''
#         for acc in self.analytic_acc_ids:
#             if acc == self.analytic_acc_ids[-1]:
#                 analytics += acc.name
#             else:
#                 analytics += acc.name + ', '
#         if len(self.report_type_ids) > 1:
#             raise Warning('You can only select one(1) Report type')
#         self.name = str(self.report_type_ids.name) + ' Report for '\
#         + analytics + ' Analytical Account(s)'

    
#     def print_report(self):
#         if not self.name:
#             pass
#             return False
        # all_journals = self.env['account.journal']
        # print(all_journals, '  ***************************')
        # journals_to_see = all_journals.filtered(lambda record:record.analytic_account_id == self.srn)
        # journals_to_see = all_journals.search([('analytic_account_id', 'in', self.analytic_acc_ids)])
        # print(journals_to_see, ' ########################')
        # journals_to_see = []
        # journal_items = self.env['account.move.line']
        # journals_to_see = [item.journal_ids for item in journal_items]
        # journals_to_see = self.env['account.journal'].search([])
        # for journal in journal_items:
        #     if journal.analytic_account_id in self.analytic_acc_ids:
        #         journals_to_see.append(journal)
        # action_to_perform = {
        #     'type': 'ir.actions.act_window',
            # 'object': 'account.balance.report',
            # 'id': ('account.action_account_balance_menu'),
            # 'views': [[False,'form']],
            # 'journal_ids': journals_to_see,
            # 'target': 'new',
            # 'action_id': '212',
            # 'view_id': 'report_trialbalance',
            # 'res_model': 'account.balance.report',
            # 'res_id': diagnosis_to_see.id,
            # }
        # print([i.default_credit_account_id.name for i in self.env['account.journal'].browse([1])], '   &&&&&&&&&&&&&&&&&')
        # return action_to_perform


class AlmTrialBalanceReport(models.TransientModel):
    _inherit = "account.balance.report"

    analytic_acc_ids = fields.Many2many('account.analytic.account', string="Analytic Account(s)")

    @api.depends('analytic_acc_ids')
    def recompute_journal_ids(self):
        valid_journal_ids = []
        journal_items = self.env['account.move.line'].search([])
        print(journal_items, ' ********************************************')
        for item in journal_items:
            if item.analytic_account_id in self.analytic_acc_ids:
                valid_journal_ids.append(item.journal_id.id)
                print(item, ' ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')   
            # else:
            #     self.analytic_acc_ids.
        valid_journal_ids = list(set(valid_journal_ids))
        print(valid_journal_ids, ' $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')   
        # journals_to_see = all_journals.search([('analytic_account_id', 'in', self.analytic_acc_ids)])
        # valid_journal_ids = account_move_line.filtered(lambda record:record.analytic_account_id in self.analytic_acc_ids)
        # journals_to_see = all_journals.filtered(lambda record:record.analytic_account_id == self.srn)
        self.journal_ids = self.env['account.journal'].browse(valid_journal_ids)
        # for analytic_acc in self.analytic_acc_ids:
        #     if analytic_acc.journal_id in self.journal_ids:
                
        print (self.journal_ids, '  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        # self.check_report()
        # if not self.journal_ids:
        #     raise Warning('Cannot print report for ')
        return self.check_report()


class AlmFinancialReport(models.TransientModel):
    _inherit = "accounting.report"

    analytic_acc_ids = fields.Many2many('account.analytic.account', string="Analytic Account(s)")

    @api.depends('analytic_acc_ids')
    def recompute_journal_ids(self):
        valid_journal_ids = []
        journal_items = self.env['account.move.line'].search([])
        print(journal_items, ' ********************************************')
        for item in journal_items:
            if item.analytic_account_id in self.analytic_acc_ids:
                valid_journal_ids.append(item.journal_id.id)
                print(item, ' ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')   
            # else:
            #     self.analytic_acc_ids.
        valid_journal_ids = list(set(valid_journal_ids))
        print(valid_journal_ids, ' $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')   
        # journals_to_see = all_journals.search([('analytic_account_id', 'in', self.analytic_acc_ids)])
        # valid_journal_ids = account_move_line.filtered(lambda record:record.analytic_account_id in self.analytic_acc_ids)
        # journals_to_see = all_journals.filtered(lambda record:record.analytic_account_id == self.srn)
        self.journal_ids = self.env['account.journal'].browse(valid_journal_ids)
        # for analytic_acc in self.analytic_acc_ids:
        #     if analytic_acc.journal_id in self.journal_ids:
                
        print (self.journal_ids, '  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        # self.check_report()
        # if not self.journal_ids:
        #     raise Warning('Cannot print report for ')
        return self.check_report()
