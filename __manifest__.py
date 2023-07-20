# -*- coding: utf-8 -*-
{
    'name': "Portal RH - CM",

    'summary': """
        Módulo Reponsável por toda a informação relativamente ao Portal RH
        """,

    'description': """
        Este Módulo é composto por:
        \n\t- Objetos:
        \n\t\t- Contact
        \n\t\t- Candidatura
        \n\t\t- Anuncio
        \nEstes Models pretendem dar suporte ao Portal RH.
    """,

    'author': "Igor Manuel Terra Matos e Jaques Alberto Ferreira Resende",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'hr_recruitment',
                'website',
                'hr',
                'contacts',
                "auth_signup",
                'website_hr_recruitment',
                'auth_api_key'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/assets.xml',
        'views/form_success.xml',
        'views/register_form.xml',
        'views/contact_form.xml',
        'views/my_account_form.xml',
        'views/navbar.xml',
        'views/views.xml',
        'views/partner_description.xml',
        'views/candidatura_details.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
}
