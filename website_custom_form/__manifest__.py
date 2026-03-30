{
    'name': "Website",

    'summary': "This module is for product management.",

    'description': "This module is for product management.",

    'author': "CandidRoot Solutions PVT LTD",
    'license': 'LGPL-3',
    'category': 'Uncategorized',
    'version': '19.0.0.1',

    'depends': ['website'],

    'data': [
        'views/template1.xml',
        'views/template.xml',
    ],

    'assets': {
        'web.assets_frontend': [
            'website_custom_form/static/src/js/address.js',
        ],
    },

    'installable': True,
    'application': True,
    'auto_install': False,
}
