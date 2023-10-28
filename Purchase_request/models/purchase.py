# -*- coding: utf-8 -*-
# Copyright 2016 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0).

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import odoo.addons.decimal_precision as dp

class PurchaseRequest(models.Model):

    _inherit = 'purchase.request'
    _description = 'Purchase Request'


     #My logic
    @api.constrains("analytic_account_id")
    def _check_for_different_tag(self):
        for r in self:
            lines = r.line_ids
            analytic_tag = lines[0].analytic_account_id.id
            for line in lines:
                if analytic_tag != line.analytic_account_id.id:
                   raise exceptions.ValidationError("You cannot use different analytic Tag")
