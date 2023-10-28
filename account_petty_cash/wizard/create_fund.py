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

from odoo import api, fields, models
from odoo.addons import decimal_precision as dp
from odoo.tools.translate import _


class CreateFundWizard(models.TransientModel):

    _name = 'account.pettycash.fund.create'
    _description = 'Petty Cash Fund Creation Wizard'

    # Fields
    #
    fund_name = fields.Char(string="Petty Cash Account name", required=True)
    fund_code = fields.Char(default="PettyC")
    fund_amount = fields.Float(string="Amount",
        digits=dp.get_precision('Product Price'), required=True)
    custodian = fields.Many2one('res.users', required=True, domain=[('groups_id','in',[73])])
    payable_account = fields.Many2one('account.account', required=True)
    effective_date = fields.Date(required=True)
    payable_move = fields.Many2one('account.move', string="Journal Entry")
    fund = fields.Many2one('account.pettycash.fund')
    analytic_account = fields.Many2one('account.analytic.account',required=True)
    analytics_tag_ids = fields.Many2one('account.analytic.tag',required = True,string="Analytic tag")

    @api.multi
    def initialize_fund(self):

        # Create the petty cash fund
        #
        FndObj = self.env['account.pettycash.fund']
        for wizard in self:
            fnd = FndObj.create_fund(
                wizard.fund_amount, wizard.fund_name,wizard.fund_code,
                wizard.custodian, wizard.payable_account,wizard.analytic_account,wizard.analytics_tag_ids)

            desc = _("Establish Petty Cash Fund (%s)" % (wizard.fund_name))

            # Create payable account entry and post it
            
            move = fnd.create_payable_journal_entry(
                fnd, wizard.payable_account.id, wizard.effective_date,
                wizard.fund_amount, desc)
            wizard.payable_move = move
            wizard.fund = fnd
