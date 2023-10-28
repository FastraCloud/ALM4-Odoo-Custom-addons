# -*- coding: utf-8 -*-
# Copyright 2017 Joaquin Gutierrez Pedrosa <joaquin@gutierrezweb.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class AccountAccount(models.Model):
    _inherit = 'account.account'


    one_digit = fields.Char(
        string='1 Digit',
        compute='_compute_digits',
        store=True,
        help="One Digit")
    two_digit = fields.Char(
        string='2 Digit',
        compute='_compute_digits',
        store=True,
        help="Two Digit")
    three_digit = fields.Char(
        string='3 Digit',
        compute='_compute_digits',
        store=True,
        help="Three Digit")
