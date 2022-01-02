# -*- coding: utf-8 -*-
{
    'name': "om_hospital",

    'summary': """This is an application for Hospital management""",
    'sequence': -10,
    'description': """
        This is an application for Hospital management
    """,

    'author': "Abdalazeem Ink",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'productivity',
    'version': '1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/patient.xml',
        'views/kids.xml',
        'views/patient_gender.xml',
        'views/appointment.xml',
        'views/sale.xml',
    ],
    'installable': True,
    'application': True,
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
