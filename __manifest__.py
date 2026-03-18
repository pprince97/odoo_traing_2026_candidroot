{
    'name': "Product Management Smit",

    'summary': "This module is for product management.",

    'description': "This module is for product management.",

    'author': "CandidRoot Solutions PVT LTD",
    'license': 'LGPL-3',
    'category': 'Uncategorized',
    'version': '19.0.0.1',

    'depends': ['base', 'web', 'product'],

    'data': [
        'security/ir.model.access.csv',
        'views/product_views.xml',
    ],



    'installable': True,
    'application': True,
    'auto_install': False,
}
