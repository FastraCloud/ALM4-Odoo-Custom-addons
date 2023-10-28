# -*- coding: utf-8 -*-
{
    'name': 'Invoice/Bills Excel Report',
    'version': '1.0',
    'category': 'Accounts',
    'summary': '''
        Prints Invoice/Bills Excel Report based on start date,end date,customer,vendor,both and you can also select
        whether the invoice state is open or paid.
        ''',
    'author': 'HK',
    'license': "OPL-1",
    'support': 'prince.odoo.up@gmail.com',
    'depends': [
        'sale',
        'purchase',
        'account_accountant'
    ],
    'data': [
        'wizard/invoice_xls_view.xml'
    ],
    'demo': [],  
    'images': ['static/description/banner.png'],
    'auto_install': False,
    'installable': True,
    'application': True
}
