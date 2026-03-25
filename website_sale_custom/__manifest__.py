{
    'name': "Website",

    'summary': "This module is for product management.",

    'description': "This module is for product management.",

    'author': "CandidRoot Solutions PVT LTD",
    'license': 'LGPL-3',
    'category': 'Uncategorized',
    'version': '19.0.0.1',

    'depends': ['website', 'library_management_smit', 'product', 'website_sale'],

    'data': [
        'security/ir.model.access.csv',
        'views/product_attribute.xml',
    ],



    'installable': True,
    'application': True,
    'auto_install': False,
}
