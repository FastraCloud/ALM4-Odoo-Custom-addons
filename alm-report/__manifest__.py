# -*- coding: utf-8 -*-
{
    'name': "alm-report",

    'summary': """
        Extends trial_balance and financial report forms, to include a field for
        analytic accounts to filter by""",

    'description': """
        This is a custom module developed by BigFix tech. to better
        enhance accounting reporting in odoo, such as trial balance, p&l and balance sheet reports.
    """,

    'author': "BigFix Integrated Tech.",
    'website': "http://www.bigfixtech.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/10.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'ALM project',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account_accountant', 'account_analytic_default', 'purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        # 'views/menu_view.xml',
        'views/templates.xml',
        'reports/alm_report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}