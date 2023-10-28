# -*- coding: utf-8 -*-
#
#
#    Copyright (c) 2016 Sucros Clear Information Technologies PLC.
#    All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify it
#    under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#

from odoo import api, exceptions, fields, models
from odoo.addons import decimal_precision as dp
from odoo.tools import float_compare
from odoo.tools.translate import _

PETTYCASH_STATE = [
    ('draft', 'Draft'),
    ('open', 'Open'),
    ('closed', 'Closed'),
]


class AccountVoucher(models.Model):

    _inherit = 'account.voucher'

    petty_cash_fund = fields.Many2one('account.pettycash.fund')

    @api.multi
    def button_cancel_voucher(self):

        for voucher in self:
            voucher.cancel_voucher()


class PettyCash(models.Model):

    _name = 'account.pettycash.fund'
    _description = 'Petty Cash Fund'
    _inherit = 'mail.thread'

    @api.multi
    def _balance(self):

        # True accounting balance is difference between
        # debits and credits minus the open vouchers.
        #
        for fund in self:
            balance = 0.0
            for move in fund.journal_entries:
                for line in move.line_ids:
                    if line.account_id.id \
                        not in [fund.journal.default_debit_account_id.id,
                                fund.journal.default_credit_account_id.id]:
                        continue
                    balance += (line.credit - line.debit)
                for v in fund.vouchers:
                    for l in v.line_ids:
                        balance += l.price_subtotal
            fund.balance = fund.amount - balance
            if balance == fund.amount:
                  fund.write({'state': 'closed', 'active': True})

    @api.multi
    def _get_entries(self):

        AccountMove = self.env['account.move']

        for fund in self:
            moves = AccountMove.search([('journal_id', '=', fund.journal.id)])
            fund.journal_entries = [(6, 0, [m.id for m in moves])]

    # Fields
    #
    name = fields.Char(required=True, readonly=True,
                       states={'draft': [('readonly', False)]})
    custodian = fields.Many2one('res.users', required=True, readonly=True,
                                states={'draft': [('readonly', False)]})
    custodian_partner = fields.Many2one(
        'res.partner', related='custodian.partner_id', readonly=True)
    journal = fields.Many2one('account.journal', required=True)
    amount = fields.Float(string='Fund Amount', readonly=True,
                          digits=dp.get_precision('Product Price'),
                          states={'draft': [('readonly', False)]})
    balance = fields.Float(string='Balance', compute=_balance, readonly=True,
                           digits=dp.get_precision('Product Price'))
    state = fields.Selection(selection=PETTYCASH_STATE, default='draft')
    active = fields.Boolean(default=True)
    company = fields.Many2one(
        'res.company',
        default=lambda self:
        self.env['res.company']._company_default_get('account.pettycash.fund'))
    vouchers = fields.One2many(
        'account.voucher', 'petty_cash_fund', readonly=True,
        domain=[('state', 'not in', ['cancel', 'posted'])])
    vouchers_history = fields.One2many(
        'account.voucher', 'petty_cash_fund', readonly=True,
        domain=[('state', 'in', ['cancel', 'posted'])])
    journal_entries = fields.Many2many(
        'account.move', compute=_get_entries, readonly=True)
    message_ids = fields.Many2one('mail.thread')
    analytic_account = fields.Many2one('account.analytic.account',required=True,string="Analytic Account")
    analytics_tag_ids = fields.Many2one('account.analytic.tag',required = True,string="Analytic Tag")


    @api.model
    def check_is_in_group(self, name, name_desc, action_desc):

        grp = self.env.ref(name)
        user_grp_ids = self.env.user.groups_id.ids
        if grp.id not in user_grp_ids:
            raise exceptions.AccessError(
                _("Only users in group %s may %s." % (name_desc, action_desc))
            )

    @api.model
    def create_journal_sequence(self, fund_name, fund_code):

        # Only the Finance manager should be allowed to proceed beyond
        # this point.
        self.check_is_in_group('account.group_account_user',
                               'Finance Manager',
                               _("create a journal sequence for a "
                                 "petty cash fund"))

        SeqObj = self.env['ir.sequence']
        seq = SeqObj.sudo().create({
            'name': fund_name,
            'code': 'pay_voucher',
            'prefix': fund_code + "/%(y)s/",
            'padding': 2,
        })
        return seq

    @api.model
    def create_journal(self, fund_name, fund_code, custodian_id, seq_id,
                       default_credit_acct_id, default_debit_acct_id):

        JrnObj = self.env['account.journal']
        jrnl = JrnObj.create({
            'name': fund_name,
            'code': fund_code,
            'type': 'cash',
            'default_credit_account_id': default_credit_acct_id,
            'default_debit_account_id': default_debit_acct_id,
            'user_id': custodian_id,
            'sequence_id': seq_id,
            'update_posted': True,
        })
        return jrnl

    @api.model
    def create_fund(self, fund_amount, fund_name,fund_code, custodian,
                    account,analytic_account,analytics_tag_ids):

        seq = self.create_journal_sequence(fund_name, fund_code)
        jrn = self.create_journal(fund_name, fund_code, custodian.id, seq.id,
                                  account.id, account.id)
        fnd = self.create({
            'name': fund_name,
            'custodian': custodian.id,
            'amount': fund_amount,
            'journal': jrn.id,
            'state': 'open',
            'analytic_account':analytic_account.id,
            'analytics_tag_ids':analytics_tag_ids.id
        })

        return fnd

    @api.multi
    def close_fund(self, date, receivable_account):

        # Only the Finance manager should be allowed to proceed beyond
        # this point.
        self.check_is_in_group('account.group_account_manager',
                               'Finance Manager',
                               _("close a petty cash fund"))

        for fund in self:
            if fund.vouchers and len(fund.vouchers) > 0:
                raise exceptions.ValidationError(
                    _("Petty Cash fund (%s) has un-reconciled vouchers" %
                      (fund.name))
                )

            desc = _("Close Petty Cash fund (%s)" % (fund.name))
          #  fund.create_receivable_journal_entry(
             #   fund, receivable_account.id, date, fund.amount, desc)

            fund.write({'state': 'closed', 'active': True})

    @api.multi
    def reopen_fund(self):

        # Only the Finance manager should be allowed to re-open a fund
        self.check_is_in_group('account.group_account_manager',
                               'Finance Manager',
                               _("re-open a petty cash fund"))

        for fund in self:
            fund.write({'state': 'open', 'active': True})

    @api.multi
    def change_fund_amount(self, new_amount):

        # Only the Finance manager should be allowed to change the
        # amount of the fund.
        self.check_is_in_group('account.group_account_manager',
                               'Finance Manager',
                               _("change the amount of a petty cash fund"))

        for fund in self:
            # If this is a decrease in funds and there are unreconciled
            # vouchers do not allow the user to proceed.
            diff = float_compare(new_amount, fund.amount, precision_digits=2)
            if diff == -1 and fund.vouchers and len(fund.vouchers) > 0:
                raise exceptions.ValidationError(
                    _("Petty Cash fund (%s) has unreconciled vouchers" %
                      (fund.name))
                )
            fund.amount = new_amount

    @api.model
    def create_journal_entry_common(
            self, _type, fnd, account_id, date, amount, desc):

        #accountMove = self.env['account.move']
        accountMove= self.env['account.move']

        # Set debit and credit accounts according to type of entry. Default
        # to payable.
        debit_account = fnd.journal.default_debit_account_id.id
        credit_account = account_id
        if _type == 'receivable':
            debit_account = account_id
            credit_account = fnd.journal.default_credit_account_id.id

        # First, create the move
        #move_vals = accountMove.account_move_prepare(
           # fnd.journal.id, date=date)
        #move_vals.update({'narration': desc})

	move_vals = {
             'name': desc,
             'journal_id': fnd.journal.id,
             'date':date}
 
 	move_vals.update({'narration':desc})
        # Create the first line
        move_line1_vals = {
            'name': desc,
            'debit': amount,
            'credit': 0.0,
            'account_id': debit_account,
            'journal_id': fnd.journal.id,
            'analytic_account_id':fnd.analytic_account.id,
             'analytics_tag_ids':fnd.analytics_tag_ids.id,           
            'partner_id': fnd.custodian_partner.id,
            'date': date,
        }
        # Create the second line
        move_line2_vals = {
            'name': desc,
            'debit': 0.0,
            'credit': amount,
            'journal_id': fnd.journal.id,
            'account_id': credit_account,
            'partner_id': fnd.custodian_partner.id,
               'analytic_account_id':fnd.analytic_account.id,
             'analytics_tag_ids':fnd.analytics_tag_ids.id, 
            'quantity': 1,
            'date': date,
            'date_maturity': date,
        }
        # Update the journal entry and post
        #
        move_vals.update({
            'line_ids': [(0, 0, move_line2_vals), (0, 0, move_line1_vals)]
        })
        move = accountMove.create(move_vals)
        move.post()
        return move

    @api.model
    def create_payable_journal_entry(
            self, fnd, account_id, date, amount, desc):

        return self.create_journal_entry_common(
            'payable', fnd, account_id, date, amount, desc)

    @api.model
    def create_receivable_journal_entry(
            self, fnd, account_id, date, amount, desc):

        return self.create_journal_entry_common(
            'receivable', fnd, account_id, date, amount, desc)

    # @api.one
    # def proposal_title_approved(self):
    #             template_obj = self.env['email.template'].sudo().search([('name', '=', 'Create Section for Thesis')], limit=1)
    #             body = template_obj.body_html
    #             body = body.replace('--department--', self.department_id.name)
    #             body = body.replace('--session--', self.session_id.name)
    #             body = body.replace('--supervisor--', self.supervisor_id.name)
    #             body = body.replace('--rollno--', self.student_id.roll_no)
    #             body = body.replace('--caseno--', self.case_no)
    #             body = body.replace('--campus--', self.campus_id.name)
    #             if template_obj:
    #                 mail_values = {
    #                     'subject': template_obj.subject,
    #                     'body_html': body,
    #                     'email_to': ';'.join(map(lambda x: x, receipt_list)),
    #                     'email_cc': ';'.join(map(lambda x: x, email_cc)),
    #                     'email_from': template_obj.email_from,
    #                 }
    #                 create_and_send_email = self.env['mail.mail'].create(mail_values).send()

    def request_approval(self):

        #print("message sent1")
        group = self.env['res.groups'].search([('category_id.name', '=', 'Accountant')])
        recipient_partners = []
        for recipient in group.users:
            recipient_partners.append(
                (4, recipient.partner_id.id)
            )
            # user_ids=self.pool.get('res.users').search(cr,uid,[('groups_id','=',manf_categ_ids)],context=context)
        post_vars = {'subject': "notification about pending petty cash fund approval",
                     'body': "Yes inform me as i belong to petty cash group",
                     'partner_ids': recipient_partners, }  # Where "4" adds the ID to the list
        # of followers and "3" is the partner ID
        thread_pool = self.pool.get('mail.thread')
        thread_pool.message_post(self,**post_vars)
        print("message sent")
        self.state = 'waiting'

 
