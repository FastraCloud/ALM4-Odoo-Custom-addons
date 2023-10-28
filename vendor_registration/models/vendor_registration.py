from odoo import fields, models


class VendorRegistration(models.Model):
    _name = 'vendor.registration'
    _description = 'Vendor Registration'

    name= fields.Char('Company Name')
    type_of_vendor= fields.Selection(
        [('manufacturer', 'Manufacturer'), ('dealer', 'Dealer'), ('stockist', 'Stockist')], string='Type of Vendor')
    major_supplier= fields.Char('Major Supplier of')
    vendor_sales_name= fields.Char('Vendor Sales Name')

    managing_director_name= fields.Char('Contact Person')
    managing_director_mobile_1= fields.Char('Mobile 1')
    managing_director_mobile_2= fields.Char('Mobile 2')
    managing_director_email= fields.Char('Email')

    person_contacted_name= fields.Char('Contact Person')
    person_contacted_mobile_1= fields.Char('Mobile 1')
    person_contacted_mobile_2= fields.Char('Mobile 2')
    person_contacted_email= fields.Char('Email')

    name_of_banker= fields.Char('Name of Banker')
    account_no= fields.Char('Account No.')
    company_address= fields.Text('Company Address')
    min_order_value= fields.Float('Min. Order Value')
    payment_term= fields.Char('Payment Terms')
    delivery_term= fields.Char('Delivery Terms')
    vat= fields.Char('Vat No.')
    overall_turn_over_for_year= fields.Char('Overall Turn-over for last 3 Financial Years')
    major_customers= fields.Char('Major Customers')
    details_of_major_project= fields.Char('Details of Major Project supplies/completed')
    items_supplied= fields.Char("Items Supplied")
    manpower= fields.Char('Manpower/Equipment/Capacity details')
    details_of_collaborators= fields.Char('Details of Collaborators and Collaborations')
    details_of_quality= fields.Char('Details of Quality Approvals')
    other_info= fields.Char('Other Information(If any)')