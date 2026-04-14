{
    'name': "Product Management Smit",

    'summary': "This module is for product management.",

    'description': "This module is for product management.",

    'author': "CandidRoot Solutions PVT LTD",
    'license': 'LGPL-3',
    'category': 'Uncategorized',
    'version': '19.0.0.1',

    'depends': ['base', 'web', 'product', 'stock', 'account'],

    'data': [
        'security/ir.model.access.csv',
        'data/rental_seq.xml',
        'views/rental_object_views.xml',
        'views/res_partner_inherit.xml',
        'views/menu_views.xml',
    ],



    'installable': True,
    'application': True,
    'auto_install': False,
}
