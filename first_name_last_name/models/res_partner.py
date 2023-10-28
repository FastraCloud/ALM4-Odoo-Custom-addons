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

import logging
_logger = logging.getLogger(__name__)
from odoo import api, fields, models, exceptions

class ResPartner(models.Model):
    """ This method will add `lastname` and `firstname`. `name` is a stored function field."""
    _inherit = 'res.partner'

    firstname = fields.Char("First name")
    lastname = fields.Char("Last name")
    name = fields.Char(
        compute="_compute_name",
        inverse="_inverse_name_after_cleaning_whitespace",
        required=False,
        store=True)

    @api.model
    def create(self, vals):
        """Override method to invert name at creation if unavailable."""
        context = dict(self.env.context)
        name = vals.get("name", context.get("default_name"))

        if name is not None:
            # Calculate the splitted fields
            inverted = self._get_inverse_name(
                self._get_whitespace_cleaned_name(name),
                vals.get("is_company",
                         self.default_get(["is_company"])["is_company"]))

            for key, value in inverted.iteritems():
                if not vals.get(key) or context.get("copy"):
                    vals[key] = value

            # Remove the combined fields
            if "name" in vals:
                del vals["name"]
            if "default_name" in context:
                del context["default_name"]

        return super(ResPartner, self.with_context(context)).create(vals)

    @api.multi
    def copy(self, default=None):
        """Override method to ensure partners are copied correctly."""
        return super(ResPartner, self.with_context(copy=True)).copy(default)

    @api.model
    def default_get(self, fields_list):
        """This method will invert `name` when getting default values."""
        result = super(ResPartner, self).default_get(fields_list)

        inverted = self._get_inverse_name(
            self._get_whitespace_cleaned_name(result.get("name", "")),
            result.get("is_company", False))

        for field in inverted.keys():
            if field in fields_list:
                result[field] = inverted.get(field)

        return result

    @api.model
    def _get_computed_name(self, lastname, firstname):
        """This method will compute the `name` from first and last names."""
        return u" ".join((p for p in (lastname, firstname) if p))

    @api.one
    @api.depends("firstname", "lastname")
    def _compute_name(self):
        """This method will re-compute and write the `name` field when it changes."""
        self.name = self._get_computed_name(self.lastname, self.firstname)

    @api.one
    def _inverse_name_after_cleaning_whitespace(self):
        # Remove unneeded whitespace
        clean = self._get_whitespace_cleaned_name(self.name)

        # Clean name avoiding infinite recursion
        if self.name != clean:
            self.name = clean

        # Save name in the real fields
        else:
            self._inverse_name()

    @api.model
    def _get_whitespace_cleaned_name(self, name):
        return u" ".join(name.split(None)) if name else name

    @api.model
    def _get_inverse_name(self, name, is_company=False):
        """ This method will compute the inverted name."""
        # Company name goes to the lastname
        if is_company or not name:
            parts = [name or False, False]
        # Guess name splitting
        else:
            parts = name.strip().split(" ", 1)
            while len(parts) < 2:
                parts.append(False)
        return {"lastname": parts[0], "firstname": parts[1]}

    @api.one
    def _inverse_name(self):
        """Try to revert the effect of :meth:`._compute_name`."""
        parts = self._get_inverse_name(self.name, self.is_company)
        self.lastname, self.firstname = parts["lastname"], parts["firstname"]

    @api.one
    @api.constrains("firstname", "lastname")
    def _check_name(self):
        if ((self.type == 'contact' or self.is_company) and not (self.firstname or self.lastname)):
            raise exceptions.UserError('Missing Last or First Name')

    @api.multi
    @api.onchange("firstname", "lastname")
    def _onchange_subnames(self):
        # Modify self's context without creating a new Environment.
        self.env.context = self.with_context(skip_onchange=True).env.context

    @api.multi
    @api.onchange("name")
    def _onchange_name(self):
        if self.env.context.get("skip_onchange"):
            # Do not skip next onchange
            self.env.context = (
                self.with_context(skip_onchange=False).env.context)
        else:
            self._inverse_name_after_cleaning_whitespace()

    @api.model
    def _install_partner_firstname(self):
        # Find records with empty firstname and lastname
        records = self.search([("firstname", "=", False),
                               ("lastname", "=", False)])

        # Force calculations there
        records._inverse_name()
        _logger.info("%d partners updated installing module.", len(records))

    _sql_constraints = [('check_name',"CHECK( 1=1 )",'Missing name')]
