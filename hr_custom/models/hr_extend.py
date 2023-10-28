from odoo import models, fields,api, _
import time
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning


class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'
    reference_name = fields.Char("Name")
    reference_address = fields.Char("Address")
    reference_email = fields.Char("Email")
    reference_phone_number = fields.Char("Phone Number")
    reference_occupation = fields.Char("Occupation")
    reference_employer_details = fields.Char("Employer's Detail")
    relationship_duration_with_reference = fields.Char("Relationship Duration")
    reference_is_guarantor = fields.Boolean()
    guarantor = fields.One2many('hr.inherit_tree', 'form_inherit')
    states_lived_in = fields.Char("States You Have Lived in")
    languages = fields.Char('Language(s)')
    will_to_serve = fields.Boolean("Are you willing to serve in any part of Nigeria?")
    reason_for_not_serving_in_Nigeria = fields.Text("If NO, Give reasons")
    employee_professional_membership = fields.One2many('professional_training.inherit', 'employee_id', string="Employee Professional Membership")
    number_of_companies_employee_worked = fields.Integer("Number of Companies Employee Worked")
    employee_working_experience = fields.One2many('employee.working.experience', 'employee_id')
    employee_current_renumeration = fields.One2many('renumeration.breakdown.list', 'employee_id')
    employee_medical_history = fields.One2many('medical.history', 'employee_id')
    employee_likes_dislikes = fields.One2many('likes.dislikes', 'employee_id')
    employee_hobbies_socials = fields.One2many('hobbies.socials', 'employee_id')
    discipline = fields.Char("Discipline")
    qualification_level = fields.Char("Level of Qualification")
    current_user = fields.Many2one('res.users', 'Current User', default=lambda self: self.env.uid)
    


class HrEmployeeInheritTree(models.Model):
    _name = 'hr.inherit_tree'

    form_inherit = fields.Many2one('hr.employee', readonly=True)
    guarantor_name = fields.Char("Name")
    guarantor_address = fields.Char("Address")
    guarantor_occupation = fields.Char("Occupation")
    guarantor_employer_details = fields.Char("Employer's Detail")
    relationship_duration_with_guarantor = fields.Char("Relationship Duration")

class ProfessionalMembershipInherit(models.Model):
    _name = 'professional_training.inherit'

    employee_id = fields.Many2one('hr.employee',string="Related Employee")
    professional_membership = fields.Char("Professional Membership/Trainings")
    date = fields.Date("Date")

class WorkingExperienceRecord(models.Model):
    _name = 'employee.working.experience'

    from_year= fields.Date(string="From")
    to_year=fields.Date(string="To")
    name_of_employer = fields.Char("Name of Employer")
    address_of_employer = fields.Text("Employer's Address")
    employer_email=fields.Char("Employer's Email Address")
    position_held= fields.Char("Position Held")
    job_description=fields.Text("Job Description")
    total_renumeration_per_annum =fields.Float("Total Renumeration per Annum")
    reason_for_leaving = fields.Text("Reasons for Leaving")
    employee_id = fields.Many2one('hr.employee',string="Related Employee")

class RenumerationList(models.Model):
    _name = 'renumeration.breakdown.list'

    employee_id = fields.Many2one('hr.employee',string="Related Employee")
    item = fields.Char(string="Item")
    amount = fields.Float(string="Amount")

class MedicalHistory(models.Model):
    _name = 'medical.history'

    employee_id = fields.Many2one('hr.employee',string="Related Employee")
    any_disability = fields.Selection([('yes','Yes'),('no','No')], string="Have you any disability?")
    serious_illness = fields.Selection([('yes','Yes'),('no','No')], string="Are you suffering from any serious illnesses?")
    type_of_serious_illness = fields.Char("What type of ailment")
    recurrent_illness = fields.Selection([('yes','Yes'),('no','No')], string="Are you suffering from any recurrent illness?")
    type_of_recurrent_illness = fields.Char("What type of ailment")
    undergo_medical_test = fields.Selection([('yes','Yes'),('no','No')], string="Are you prepared to undergo medical test?")

class HobbiesAndSocials(models.Model):
    _name = 'hobbies.socials'

    hobbies = fields.Char("Hobbies")
    socials = fields.Char("Socials")
    employee_id = fields.Many2one('hr.employee', string="Related Employee")

class LikesAndDislikes(models.Model):
    _name = 'likes.dislikes'

    likes = fields.Char("Likes")
    dislikes = fields.Char("Dislikes")
    employee_id = fields.Many2one('hr.employee', string="Related Employee")

#class EducationQualification(models.Model):
 #   _name = 'education.qualification'

 #   discipline = fields.Char("Discipline")
  #  qualification_level = fields.Char("Level of Qualification")
   # employee_id = fields.Many2one('hr.employee',string="Related Employee")
