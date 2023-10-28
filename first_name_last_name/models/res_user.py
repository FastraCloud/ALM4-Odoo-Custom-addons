# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (https://opensource.org/licenses/LGPL-3.0).
#
#This software and associated files (the "Software") may only be used (executed,
#modified, executed after modifications) if you have purchased a valid license
#from the authors, typically via Odoo Apps, or if you have received a written
#agreement from the authors of the Software (see the COPYRIGHT section below).
#
#You may develop Odoo modules that use the Software as a library (typically
#by depending on it, importing it and using its resources), but without copying
#any source code or material from the Software. You may distribute those
#modules under the license of your choice, provided that this license is
#compatible with the terms of the Odoo Proprietary License (For example:
#LGPL, MIT, or proprietary licenses similar to this one).
#
#It is forbidden to publish, distribute, sublicense, or sell copies of the Software
#or modified copies of the Software.
#
#The above copyright notice and this permission notice must be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
#ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#DEALINGS IN THE SOFTWARE.
#
#########COPYRIGHT#####
# © 2016 Bernard K Too<bernard.too@optima.co.ke>
#import logging
#_logger = logging.getLogger(__name__)

from odoo import api, models


class res_users(models.Model):
    _inherit = 'res.users'

    @api.model
    def default_get(self, fields_list):
        """This method will invert name when getting default values."""
        result = super(res_users, self).default_get(fields_list)

        inverted = self.env['res.partner']._get_inverse_name(self.env['res.partner']._get_whitespace_cleaned_name(result.get("name", "")), result.get("is_company", False))

        for field in inverted.keys():
            if field in fields_list:
                result[field] = inverted.get(field)

        return result

    @api.multi
    @api.onchange('firstname', 'lastname')
    def _compute_name(self):
        """This method will write the 'name' field according to splitted data."""
        for rec in self:
            rec.name = rec.partner_id._get_computed_name(
                rec.lastname, rec.firstname)
