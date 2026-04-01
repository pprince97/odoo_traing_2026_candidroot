{
    'name': "Owl Template",

    'summary': "This module is for understanding the purpose of owl.",

    'description': "This module is for understanding the purpose of owl.",

    'author': "CandidRoot Solutions PVT LTD",
    'license': 'LGPL-3',
    'category': 'Uncategorized',
    'version': '19.0.0.1',

    'depends': ['website'],

    'data': [
        'views/action.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'owl_template1/static/src/js/counter.js',
            'owl_template1/static/src/js/product_card.js',
            'owl_template1/static/src/css/counter.css',
        ]
    },

    'installable': True,
    'application': True,
    'auto_install': False,
}
