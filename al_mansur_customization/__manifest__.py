# -*- coding: utf-8 -*-
{
    'name': "ALM CUSTOMISATION(EXTENDED)",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/10.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'
                ,'account','payment','account_voucher','purchase_request','sale','mrp','kay_petty_cash'],

    # always loaded
    'data': [
	 'security/rule.xml',
         'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
	'views/batching_view.xml',
	
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
     ],
}
