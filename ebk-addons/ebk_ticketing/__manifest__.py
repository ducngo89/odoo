# -*- coding: utf-8 -*-
{
    'name': "EBK TRAVEL",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail','website','sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/transaction.xml',
        'views/balance.xml',
        'views/booking.xml',
        'views/passenger.xml',
        'wizards/topup_agent.xml',
        'wizards/topup_supplier.xml',
        'wizards/topup_payment.xml',
        'wizards/topup_transfer.xml',
        'views/settings.xml',
        'views/templates.xml',
        'views/assets.xml',
        'views/product.xml',
        'views/menus.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True
}
